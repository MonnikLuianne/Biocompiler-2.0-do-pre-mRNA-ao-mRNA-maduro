import streamlit as st
import pandas as pd
import base64
import os

from biocompiler import processar_sequencia


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="BioCompiler 2.0",
    page_icon="🧬",
    layout="wide"
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def ler_arquivo(caminho):

    with open(caminho, "r", encoding="utf-8") as arquivo:

        return [
            linha.strip()
            for linha in arquivo
            if linha.strip()
        ]


def processar_entrada(pre_rna):

    return processar_sequencia(pre_rna)

def destacar_erro(sequencia, resultado):

    sequencia = sequencia.replace(
        "<",
        "&lt;"
    ).replace(
        ">",
        "&gt;"
    )


    # BUG - sítio 5' ausente
    # Existe AG, mas não há GU anterior compatível.
    # Destaca o AG encontrado.
    if resultado == "BUG - sítio 5' ausente":

        if "AG" in sequencia:

            sequencia = sequencia.replace(
                "AG",
                "<span style='color:red;font-weight:bold'>AG</span>",
                1
            )

        return sequencia



    # BUG - branch point
    # Não existe adenina válida entre 10 e 30 nt antes do AG.
    # Não destaca uma adenina arbitrária.
    elif resultado == "BUG - branch point":

        return sequencia



    # BUG - sítio 3' ausente
    # Existe GU, mas não há AG posterior compatível.
    # Destaca o GU encontrado.
    elif resultado == "BUG - sítio 3' ausente":

        if "GU" in sequencia:

            sequencia = sequencia.replace(
                "GU",
                "<span style='color:red;font-weight:bold'>GU</span>",
                1
            )

        return sequencia



    # CORRETO ou outro diagnóstico
    else:

        return sequencia


def gerar_diagnostico(resultados):

    diagnosticos = {

        "CORRETO": 0,

        "BUG - sítio 5' ausente": 0,

        "BUG - branch point": 0,

        "BUG - sítio 3' ausente": 0

    }


    for resultado in resultados:

        tipo = resultado["Resultado"]

        if tipo in diagnosticos:

            diagnosticos[tipo] += 1


    return diagnosticos


def gerar_arquivo_exportacao(resultados):

    linhas = []

    linhas.append(
        "linha;status;resultado;mRNA_maduro"
    )


    for resultado in resultados:

        if resultado["Status"] == "CORRETO":
            status_exportado = "OK"
            mrna_exportado = resultado["mRNA maduro"]
        else:
            status_exportado = "ERRO"
            mrna_exportado = "NÃO GERADO"

        linhas.append(

            f"{resultado['Entrada']};"
            f"{status_exportado};"
            f"{resultado['Resultado']};"
            f"{mrna_exportado}"

        )


    return "\n".join(linhas)



# ============================================================
# FUNDO
# ============================================================

imagem_fundo = "foto_fundo_escura.jpg"


if os.path.exists(imagem_fundo):

    with open(imagem_fundo, "rb") as arquivo:

        imagem_base64 = base64.b64encode(
            arquivo.read()
        ).decode()


    st.markdown(

        f"""

<style>

.stApp {{

background-image:

linear-gradient(
rgba(0,20,50,0.15),
rgba(0,20,50,0.15)
),

url("data:image/jpg;base64,{imagem_base64}");

background-size:cover;

background-position:center;

}}


h1,h2,h3,p,label {{

color:white !important;

text-shadow:
0 2px 5px black;

}}

/* ====================================================
   MÉTRICAS
   ==================================================== */

div[data-testid="stMetricLabel"] {{

color:white !important;

text-shadow:
0 2px 5px black;

}}


div[data-testid="stMetricValue"] {{

color:white !important;

text-shadow:
0 2px 5px black;

}}

/* ====================================================
   EXPANDER - DETALHAMENTO
   ==================================================== */

div[data-testid="stExpander"] {{

background:
rgba(255,255,255,0.95) !important;

border-radius:10px;

border:1px solid rgba(255,255,255,0.4);

}}



div[data-testid="stExpander"] summary {{

color:black !important;

font-weight:700;

}}



div[data-testid="stExpander"] p {{

color:black !important;

text-shadow:none !important;

}}



div[data-testid="stExpander"] div {{

color:black !important;

}}


</style>

        """,

        unsafe_allow_html=True

    )



# ============================================================
# CABEÇALHO
# ============================================================

st.title("🧬 BioCompiler 2.0")

st.subheader(
    "RNA Processor"
)

st.write(
    "Sistema para processamento de pré-mRNA até mRNA maduro."
)


st.divider()



# ============================================================
# ENTRADAS
# ============================================================


st.header("📂 Entradas")


nome_arquivo = "BioCompiler2_entrada_40_casos_modelo_oficial.txt"


caminho = os.path.join(
    os.path.dirname(__file__),
    nome_arquivo
)



try:

    entradas = ler_arquivo(caminho)


except Exception as erro:

    st.error(
        f"Erro ao carregar arquivo: {erro}"
    )

    entradas = []



col1,col2 = st.columns(2)


with col1:

    st.metric(
        "Entradas carregadas",
        len(entradas)
    )


with col2:

    st.metric(
        "Formato",
        "TXT"
    )



st.divider()



# ============================================================
# EXECUÇÃO
# ============================================================


st.header("▶ Execução")


if st.button(
    "▶ Iniciar execução",
    type="primary",
    use_container_width=True
):


    resultados = []


    barra = st.progress(0)



    for numero, pre_rna in enumerate(
        entradas,
        start=1
    ):


        resultado = processar_entrada(
            pre_rna
        )


        resultados.append({

            "Entrada": numero,

            "Pré-mRNA": pre_rna,

            "Status": resultado["status"],

            "Resultado": resultado["resultado"],

            "mRNA maduro": resultado["mrna_maduro"]

        })


        barra.progress(
            numero / len(entradas)
        )



    st.success(
        "Execução concluída!"
    )



    # ========================================================
    # RESULTADOS
    # ========================================================


    st.divider()

    st.header(
        "📋 Resultados"
    )


    df = pd.DataFrame(resultados)


    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # DETALHAMENTO
    # ========================================================


    st.divider()

    st.header(
        "🔬 Detalhamento"
    )


    for resultado in resultados:


        with st.expander(
            f"Entrada {resultado['Entrada']} - {resultado['Resultado']}"
        ):


            st.markdown(

                f"""
                **Pré-mRNA:**

                <span style="font-family:monospace">

                {destacar_erro(
                    resultado['Pré-mRNA'],
                    resultado['Resultado']
                )}

                </span>
                """,

                unsafe_allow_html=True

            )


            st.write(
                f"**Status:** {resultado['Status']}"
            )



            if resultado["Status"] == "CORRETO":


                st.write(
                    "**Sítio 5':** OK"
                )


                st.write(
                    "**Branch point:** OK"
                )


                st.write(
                    "**Sítio 3':** OK"
                )


                st.write(
                    "**Splicing:** OK"
                )


                st.write(
                    "**CAP 5': ADICIONADA**"
                )


                st.write(
                    "**Cauda poli-A: 100 A**"
                )


                st.write(

                    f"**mRNA maduro:** "
                    f"{resultado['mRNA maduro']}"

                )

            else:


                st.write(

                    f"**Diagnóstico:** "
                    f"{resultado['Resultado']}"

                )


    # ========================================================
    # RELATÓRIO
    # ========================================================


    st.divider()

    st.header(
        "📊 Relatório diagnóstico"
    )


    diagnostico = {}


    for resultado in resultados:

        tipo = resultado["Resultado"]

        diagnostico[tipo] = diagnostico.get(tipo,0)+1



    col1,col2,col3 = st.columns(3)


    with col1:

        st.metric(
            "Total",
            len(resultados)
        )


    with col2:

        st.metric(
            "Corretos",
            diagnostico.get("CORRETO",0)
        )


    with col3:

        st.metric(
            "Erros",
            len(resultados)-diagnostico.get("CORRETO",0)
        )



    st.dataframe(

        pd.DataFrame(
            {
                "Diagnóstico":list(diagnostico.keys()),
                "Quantidade":list(diagnostico.values())
            }
        ),

        hide_index=True

    )



    # ========================================================
    # EXPORTAÇÃO
    # ========================================================


    st.divider()

    st.header(
        "📥 Exportação"
    )


    arquivo = gerar_arquivo_exportacao(
        resultados
    )


    st.download_button(

        "📥 Baixar resultados",

        arquivo,

        file_name="resultados.txt",

        mime="text/plain"

    )