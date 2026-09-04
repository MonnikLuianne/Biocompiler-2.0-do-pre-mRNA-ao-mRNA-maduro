from pathlib import Path

CAP_5 = "m7Gppp"
TAMANHO_CAuda_POLI_A = 100
BASES_RNA = {"A", "U", "C", "G"}

def validar_caracteres(sequencia):
    return all(base in BASES_RNA for base in sequencia)

def encontrar_sitios_5(sequencia):
    return [i for i in range(len(sequencia) - 1) if sequencia[i:i + 2] == "GU"]

def encontrar_sitios_3(sequencia):
    return [i for i in range(len(sequencia) - 1) if sequencia[i:i + 2] == "AG"]

def encontrar_branch_points(sequencia, inicio_intron, inicio_ag):
    branch_points = []
    inicio_busca = inicio_intron + 2
    fim_busca = inicio_ag

    for pos in range(inicio_busca, fim_busca):
        if sequencia[pos] == "A":
            distancia = inicio_ag - pos
            if 10 <= distancia <= 30:
                branch_points.append(pos)

    return branch_points

def encontrar_candidatos_intron(sequencia):
    sitios_5 = encontrar_sitios_5(sequencia)
    sitios_3 = encontrar_sitios_3(sequencia)
    candidatos = []

    for inicio_gu in sitios_5:
        for inicio_ag in sitios_3:
            if inicio_ag <= inicio_gu + 1:
                continue

            branch_points = encontrar_branch_points(
                sequencia, inicio_gu, inicio_ag
            )

            if branch_points:
                candidatos.append({
                    "inicio": inicio_gu,
                    "fim": inicio_ag,
                    "branch_points": branch_points
                })

    return candidatos

def fazer_splicing(sequencia, inicio, fim):
    inicio_exon2 = fim + 2
    exon1 = sequencia[:inicio]
    exon2 = sequencia[inicio_exon2:]
    return exon1 + exon2

def adicionar_cap(sequencia):
    return CAP_5 + sequencia

def adicionar_cauda_poli_a(sequencia):
    return sequencia + ("A" * TAMANHO_CAuda_POLI_A)

def gerar_mrna_maduro(sequencia_processada):
    sequencia_com_cap = adicionar_cap(sequencia_processada)
    return adicionar_cauda_poli_a(sequencia_com_cap)

def processar_sequencia(sequencia):
    if not validar_caracteres(sequencia):
        return {
            "status": "ERRO",
            "resultado": "BUG - caracteres inválidos",
            "mrna_maduro": None
        }

    sitios_5 = encontrar_sitios_5(sequencia)

    if not sitios_5:
        return {
            "status": "ERRO",
            "resultado": "BUG - sítio 5'",
            "mrna_maduro": None
        }

    sitios_3 = encontrar_sitios_3(sequencia)
    tem_ag_depois = False

    for gu in sitios_5:
        for ag in sitios_3:
            if ag > gu + 1:
                tem_ag_depois = True
                break
        if tem_ag_depois:
            break

    if not tem_ag_depois:
        for gu in sitios_5:
            nucleotideos_apos_gu = len(sequencia) - (gu + 2)

            if nucleotideos_apos_gu < 12:
                return {
                    "status": "ERRO",
                    "resultado": "BUG - sítio 5'",
                    "mrna_maduro": None
                }

            if nucleotideos_apos_gu == 12:
                return {
                    "status": "ERRO",
                    "resultado": "BUG - íntron incompleto",
                    "mrna_maduro": None
                }

        return {
            "status": "ERRO",
            "resultado": "BUG - sítio 3'",
            "mrna_maduro": None
        }

    candidatos = encontrar_candidatos_intron(sequencia)

    if len(candidatos) == 0:
        return {
            "status": "ERRO",
            "resultado": "BUG - branch point",
            "mrna_maduro": None
        }

    if len(candidatos) > 1:
        return {
            "status": "AMBÍGUO",
            "resultado": "AMBÍGUO - splicing alternativo",
            "mrna_maduro": None
        }

    candidato = candidatos[0]
    rna_splicado = fazer_splicing(
        sequencia,
        candidato["inicio"],
        candidato["fim"]
    )

    mrna_maduro = gerar_mrna_maduro(rna_splicado)

    return {
        "status": "CORRETO",
        "resultado": "CORRETO",
        "mrna_maduro": mrna_maduro
    }

def processar_arquivo(caminho_arquivo):
    caminho = Path(caminho_arquivo)

    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    resultados = []

    with open(caminho, "r", encoding="utf-8") as arquivo:
        for numero, linha in enumerate(arquivo, start=1):
            sequencia = linha.strip()
            resultado = processar_sequencia(sequencia)
            resultado["linha"] = numero
            resultados.append(resultado)

    return resultados

def exibir_resultado(numero, resultado):
    print("=" * 60)
    print(f"ENTRADA: {numero}")
    print(f"STATUS: {resultado['status']}")

    if resultado["status"] == "CORRETO":
        print("Sítio 5': OK")
        print("Branch point: OK")
        print("Sítio 3': OK")
        print("Splicing: OK")
        print("CAP 5': ADICIONADA")
        print("Cauda poli-A: 100 A")
        print(f"mRNA MADURO: {resultado['mrna_maduro']}")
    else:
        print(f"TIPO: {resultado['resultado']}")
        print(f"mRNA maduro: {resultado['mrna_maduro']}")

def exportar_resultados(resultados, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write("linha;status;resultado;mRNA_maduro\n")

        for resultado in resultados:
            arquivo.write(
                f"{resultado['linha']};"
                f"{resultado['status']};"
                f"{resultado['resultado']};"
                f"{resultado['mrna_maduro']}\n"
            )

def mostrar_resumo(resultados):
    contagem = {}

    for resultado in resultados:
        tipo = resultado["resultado"]
        contagem[tipo] = contagem.get(tipo, 0) + 1

    print("\n" + "=" * 60)
    print("RESUMO DO PROCESSAMENTO")
    print("=" * 60)

    tipos = [
        "CORRETO",
        "BUG - sítio 5'",
        "BUG - branch point",
        "BUG - sítio 3'",
        "BUG - íntron incompleto",
        "AMBÍGUO - splicing alternativo"
    ]

    for tipo in tipos:
        print(f"{tipo}: {contagem.get(tipo, 0)}")

    print("-" * 60)
    print(f"TOTAL: {len(resultados)}")
    print("=" * 60)

if __name__ == "__main__":
    print("=" * 60)
    print("BIOCOMPILER 2.0 - RNA PROCESSOR")
    print("=" * 60)

    arquivo_entrada = "BioCompiler_2_0_entrada_60_casos.txt"
    arquivo_saida = "resultados.txt"

    try:
        resultados = processar_arquivo(arquivo_entrada)

        for resultado in resultados:
            exibir_resultado(resultado["linha"], resultado)

        exportar_resultados(resultados, arquivo_saida)
        mostrar_resumo(resultados)

        print(f"\nArquivo gerado: {arquivo_saida}")

    except FileNotFoundError as erro:
        print(f"\nERRO:\n{erro}")

    except Exception as erro:
        print(f"\nERRO INESPERADO:\n{erro}")