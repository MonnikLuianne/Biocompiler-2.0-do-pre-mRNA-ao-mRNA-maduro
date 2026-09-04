# 🧬 BioCompiler 2.0

## RNA Processor

O **BioCompiler 2.0** é um sistema desenvolvido em Python para **validação, análise e processamento de sequências de pre-mRNA**, realizando a identificação de sinais de splicing e a geração do **mRNA maduro**.

O sistema recebe um conjunto de **60 sequências de pre-mRNA**, realiza uma sequência de verificações e classifica cada entrada de acordo com os possíveis problemas encontrados.

Quando uma entrada é considerada correta, o sistema realiza o **splicing**, removendo o íntron e unindo os éxons. Em seguida, adiciona a representação didática da **CAP 5' (m7Gppp)** e uma **cauda poli-A contendo exatamente 100 adeninas**, gerando o mRNA maduro.

---

# 🎯 Objetivo do projeto

O objetivo do **BioCompiler 2.0** é desenvolver uma aplicação capaz de analisar sequências de pre-mRNA e identificar possíveis problemas relacionados aos sinais de splicing.

Para cada entrada, o sistema realiza as seguintes verificações:

1. Validação das bases de RNA;
2. Identificação do sítio 5' (`GU`);
3. Identificação do sítio 3' (`AG`);
4. Verificação da existência de um branch point válido;
5. Identificação de possíveis estruturas de íntron;
6. Detecção de íntron incompleto;
7. Detecção de múltiplas possibilidades de splicing;
8. Classificação da entrada;
9. Realização do splicing quando a entrada é considerada correta;
10. Adição da CAP 5' (`m7Gppp`);
11. Adição da cauda poli-A com 100 adeninas;
12. Geração do mRNA maduro.

O sistema também permite:

- processar as 60 entradas;
- acompanhar os resultados de cada entrada;
- visualizar o diagnóstico;
- identificar o tipo de problema encontrado;
- visualizar o mRNA maduro quando a entrada é correta;
- exportar os resultados para um arquivo `.txt`.

---

# 📄 Descrição dos arquivos

## biocompiler.py

Contém a lógica principal do BioCompiler 2.0.

Entre as principais funções estão:

`validar_caracteres()`

Valida se a sequência contém somente bases de RNA válidas:

`A`, `U`, `C` e `G`.

`encontrar_sitios_5()`

Localiza os sítios 5' representados pela sequência `GU`.

`encontrar_sitios_3()`

Localiza os sítios 3' representados pela sequência `AG`.

`encontrar_branch_points()`

Procura possíveis branch points e verifica se a adenina está entre 10 e 30 nucleotídeos antes do `AG` terminal.

`encontrar_candidatos_intron()`

Identifica estruturas de íntron no formato:

`GU ... A ... AG`

considerando as regras do branch point.

`fazer_splicing()`

Remove o íntron, incluindo os sinais `GU` e `AG`, e une os éxons.

`adicionar_cap()`

Adiciona a representação didática da CAP 5':

`m7Gppp`

`adicionar_cauda_poli_a()`

Adiciona exatamente 100 adeninas ao final da sequência.

`gerar_mrna_maduro()`

Combina a sequência processada com a CAP 5' e a cauda poli-A.

`processar_sequencia()`

Executa todo o processo de validação, classificação, splicing e geração do mRNA maduro.

`processar_arquivo()`

Lê o arquivo de entrada e processa cada sequência individualmente.

`exportar_resultados()`

Gera o arquivo contendo os resultados das 60 entradas.

`mostrar_resumo()`

Apresenta a quantidade de ocorrências de cada classificação.

---

## app.py

Responsável pela interface gráfica do sistema utilizando Streamlit.

Principais responsabilidades:

- configuração da página;
- criação da interface;
- carregamento das entradas;
- execução dos casos;
- apresentação dos resultados;
- apresentação do diagnóstico;
- visualização do mRNA maduro;
- exportação dos resultados.

---

## fundo_biocompiler.png

Imagem utilizada como plano de fundo da interface gráfica.

Deve permanecer na mesma pasta do `app.py`.

---

## BioCompiler_2_0_entrada_60_casos.txt

Contém as **60 sequências de pre-mRNA** utilizadas para testar o sistema.

Cada linha representa uma entrada independente.

O arquivo deve permanecer na mesma pasta do projeto.

---

# 🧬 Funcionamento do BioCompiler

O processamento de cada sequência segue uma ordem definida.

```text
                    SEQUÊNCIA DE pre-mRNA
                            │
                            ▼
                  ┌─────────────────────┐
                  │ Bases válidas?      │
                  │ A, U, C ou G        │
                  └──────────┬──────────┘
                             │
                       NÃO ──┴── SIM
                       │          │
                       ▼          ▼
              CARACTERES      Procurar GU
               INVÁLIDOS          │
                                  ▼
                         ┌─────────────────┐
                         │ Existe GU?      │
                         └────────┬────────┘
                                  │
                         NÃO ─────┴───── SIM
                         │                │
                         ▼                ▼
                   BUG - sítio 5'    Procurar AG
                                          │
                                          ▼
                              ┌─────────────────────┐
                              │ Existe AG depois    │
                              │ de algum GU?        │
                              └──────────┬──────────┘
                                         │
                              NÃO ───────┴────── SIM
                              │                    │
                              ▼                    ▼
                       Analisar estrutura    Procurar branch
                              │                  point
                              │                    │
                    ┌─────────┼─────────┐          ▼
                    │         │         │   ┌──────────────┐
                   <12       =12       >12 │ Candidatos?  │
                    │         │         │   └──────┬───────┘
                    ▼         ▼         ▼          │
                 sítio 5'  íntron    sítio 3'     │
                            incompleto             │
                                           ┌───────┼────────┐
                                           │       │        │
                                          0       1        >1
                                           │       │        │
                                           ▼       ▼        ▼
                                      branch    CORRETO  AMBÍGUO
                                      point
                                           │
                                           ▼
                                       SPLICING
                                           │
                                           ▼
                                    Adicionar CAP 5'
                                           │
                                           ▼
                                  Adicionar 100 A
                                           │
```

### ⚠️ Classificações

O BioCompiler 2.0 pode produzir as seguintes classificações:

 ✅ CORRETO

A sequência possui uma estrutura válida de splicing e existe apenas uma possibilidade válida de processamento.

O sistema realiza o splicing e gera o mRNA maduro.

 ❌ BUG - sítio 5'

O sítio 5', representado por GU, está ausente, alterado ou não possui estrutura suficiente para iniciar corretamente o íntron.

 ❌ BUG - branch point

Existe uma estrutura com GU e AG, mas não foi encontrado um branch point válido de acordo com a regra estabelecida.

 ❌ BUG - sítio 3'

Existe um sítio 5' (GU), mas não foi encontrado um sítio 3' (AG) válido posteriormente.

 ❌ BUG - íntron incompleto

A sequência apresenta um início de íntron (GU), porém a estrutura não possui nucleotídeos suficientes para formar um íntron completo.

 ⚠️ AMBÍGUO - splicing alternativo

A sequência apresenta mais de uma possibilidade válida de processamento.

### ▶️ Como executar o projeto
1. Clonar o repositório
git clone https://github.com/MonnikLuianne/Biocompiler-2.0-do-pre-mRNA-ao-mRNA-maduro.git
2. Acessar a pasta do projeto
cd Biocompiler-2.0-do-pre-mRNA-ao-mRNA-maduro
3. Criar o ambiente virtual

# No Windows:

python -m venv .venv
4. Ativar o ambiente virtual

# No Windows:
.venv\Scripts\activate

5. Instalar as dependências
pip install -r requirements.txt

7. Executar o processamento
python biocompiler.py

O sistema realizará o processamento das 60 sequências presentes no arquivo:

 BioCompiler_2_0_entrada_60_casos.txt

Os resultados serão apresentados no terminal e também será gerado o arquivo:
 resultados.txt
 
7. Executar a interface gráfica
Caso o arquivo app.py esteja disponível no projeto:

 streamlit run app.py

Após executar o comando, o Streamlit abrirá a aplicação no navegador.

### 🖥️ Utilização do sistema

Na interface do BioCompiler 2.0:

Clique no botão para iniciar o processamento;
O sistema processará as 60 entradas;
Cada entrada será classificada;
O diagnóstico será apresentado;
Para as entradas CORRETO, será apresentado o mRNA maduro;
O usuário poderá consultar os resultados;
Os resultados poderão ser exportados.
📄 Exportação dos resultados

O sistema possui uma opção para exportar os resultados do processamento.

Ao executar o processamento, será gerado o arquivo:

resultados.txt

O arquivo contém informações referentes às 60 entradas, incluindo:

número da entrada;
status do processamento;
resultado do diagnóstico;
mRNA maduro, quando aplicável.

O formato utilizado é:

linha;status;resultado;mRNA_maduro
                                           ▼
                                      mRNA MADURO
