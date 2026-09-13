# 🧬 BioCompiler 2.0

## RNA Processor

O **BioCompiler 2.0** é um sistema desenvolvido em Python para **validação, análise e processamento de sequências de pré-mRNA**, simulando de forma didática o processo de maturação até a geração do **mRNA maduro**.

O sistema recebe um conjunto de **40 sequências de pré-mRNA**, processando cada linha de forma independente e na ordem em que aparece no arquivo de entrada.

Durante o processamento, o BioCompiler identifica e valida os principais sinais de splicing utilizando a seguinte gramática simplificada:

```text
GU ... A ... AG
```

Onde:

- `GU` representa o sítio 5' do íntron;
- `A` representa o branch point;
- `AG` representa o sítio 3' do íntron.

Para que o branch point seja considerado válido, a adenina deve estar localizada entre **10 e 30 nucleotídeos antes do AG terminal do íntron**.

Quando uma entrada é considerada correta, o sistema realiza o **splicing**, removendo o íntron, incluindo `GU` e `AG`, e unindo diretamente os éxons adjacentes.

Em seguida, adiciona:

- a representação didática da **CAP 5' (`m7Gppp`)**;
- uma **cauda poli-A contendo exatamente 100 adeninas**.

O resultado final é o **mRNA maduro**.

---

# 🎯 Objetivo do projeto

O objetivo do **BioCompiler 2.0** é desenvolver uma aplicação capaz de receber sequências de pré-mRNA, reconhecer sinais de splicing e simular computacionalmente o processo de maturação do RNA.

Para cada entrada, o sistema realiza as seguintes etapas:

1. Validação das bases de RNA;
2. Identificação do sítio 5' (`GU`);
3. Identificação do sítio 3' (`AG`);
4. Verificação da ordem correta entre `GU` e `AG`;
5. Busca por um branch point válido;
6. Identificação de uma estrutura de íntron no formato `GU ... A ... AG`;
7. Classificação da entrada;
8. Remoção do íntron quando a entrada é válida;
9. União dos éxons;
10. Adição da CAP 5' (`m7Gppp`);
11. Adição da cauda poli-A com exatamente 100 adeninas;
12. Geração do mRNA maduro;
13. Geração de relatório com os resultados.

O sistema também permite:

- processar as 40 entradas oficiais;
- acompanhar os resultados de cada entrada;
- visualizar o diagnóstico individual;
- identificar o tipo de problema encontrado;
- visualizar o mRNA maduro quando a entrada é correta;
- visualizar um resumo do processamento;
- exportar os resultados para um arquivo `.txt`.

---

# 📄 Descrição dos arquivos

## `biocompiler.py`

Contém a lógica principal do BioCompiler 2.0.

Entre as principais funções estão:

### `validar_caracteres()`

Valida se a sequência contém somente bases de RNA válidas:

```text
A, U, C e G
```

### `encontrar_sitios_5()`

Localiza os sítios 5' representados pela sequência:

```text
GU
```

### `encontrar_sitios_3()`

Localiza os sítios 3' representados pela sequência:

```text
AG
```

### `encontrar_branch_points()`

Procura possíveis branch points e verifica se a adenina está localizada entre **10 e 30 nucleotídeos antes do `AG` terminal**.

### `encontrar_candidatos_intron()`

Identifica estruturas válidas de íntron no formato:

```text
GU ... A ... AG
```

considerando a posição dos sítios de splicing e a regra do branch point.

### `fazer_splicing()`

Remove todo o íntron, incluindo os sinais `GU` e `AG`, e une diretamente os éxons adjacentes.

Exemplo:

```text
ANTES:
EXON1 [GU ... A ... AG] EXON2

DEPOIS:
EXON1EXON2
```

### `adicionar_cap()`

Adiciona a representação didática da CAP 5':

```text
m7Gppp
```

### `adicionar_cauda_poli_a()`

Adiciona exatamente **100 adeninas** ao final da sequência.

### `gerar_mrna_maduro()`

Combina a sequência após o splicing com a CAP 5' e a cauda poli-A.

O resultado segue a estrutura:

```text
m7Gppp + SEQUÊNCIA PROCESSADA + 100 A
```

### `processar_sequencia()`

Executa o fluxo principal de validação, reconhecimento dos sinais de splicing, diagnóstico e geração do mRNA maduro.

### `processar_arquivo()`

Lê o arquivo de entrada e processa cada sequência individualmente, preservando a ordem das entradas.

### `exibir_resultado()`

Exibe no terminal o resultado detalhado do processamento de cada entrada.

### `exportar_resultados()`

Gera o arquivo `resultados.txt` contendo os resultados do processamento.

### `mostrar_resumo()`

Apresenta a quantidade de ocorrências de cada classificação e o total de entradas processadas.

---

## `app.py`

Responsável pela interface gráfica do sistema utilizando **Streamlit**.

Suas principais responsabilidades são:

- configuração da página;
- carregamento das entradas;
- execução das sequências;
- apresentação dos resultados;
- detalhamento individual das entradas;
- visualização dos diagnósticos;
- visualização do mRNA maduro;
- apresentação do relatório diagnóstico;
- exportação dos resultados.

---

## `foto_fundo_escura.jpg`

Imagem utilizada como plano de fundo da interface gráfica.

O arquivo deve permanecer na mesma pasta do `app.py`.

---

## `BioCompiler2_entrada_40_casos_modelo_oficial.txt`

Contém as **40 sequências oficiais de pré-mRNA** utilizadas para testar o sistema.

Cada linha representa uma entrada independente.

O programa processa as sequências na ordem em que aparecem no arquivo.

O arquivo deve permanecer na mesma pasta do projeto.

---

## `requirements.txt`

Contém as dependências necessárias para executar a aplicação.

Dependências utilizadas pelo projeto:

```text
streamlit
pandas
```

---

# 🧬 Funcionamento do BioCompiler

O processamento de cada sequência segue o seguinte fluxo:

```text
                     SEQUÊNCIA DE pré-mRNA
                              │
                              ▼
                    ┌───────────────────┐
                    │  Bases válidas?   │
                    │   A, U, C ou G    │
                    └─────────┬─────────┘
                              │
                        NÃO ──┴── SIM
                         │         │
                         ▼         ▼
                    ERRO DE     Localizar
                    VALIDAÇÃO    GU e AG
                                   │
                                   ▼
                       ┌───────────────────────┐
                       │ Existe GU anterior a │
                       │ um AG compatível?    │
                       └──────────┬────────────┘
                                  │
                        NÃO ──────┴────── SIM
                         │                 │
                         ▼                 ▼
               Analisar qual sítio    Procurar A válido
                  está ausente          entre 10 e 30 nt
                         │              antes do AG
                ┌────────┴───────┐          │
                │                │          ▼
                ▼                ▼   ┌─────────────────┐
          Existe AG?        Existe GU? │ Branch point   │
                │                │     │    válido?     │
                ▼                ▼     └────────┬────────┘
         BUG - sítio 5'   BUG - sítio 3'       │
             ausente          ausente      NÃO ─┴─ SIM
                                             │      │
                                             ▼      ▼
                                           BUG -  ÍNTRON
                                          branch   VÁLIDO
                                           point     │
                                                     ▼
                                                  SPLICING
                                                     │
                                                     ▼
                                              Unir os éxons
                                                     │
                                                     ▼
                                            Adicionar CAP 5'
                                                m7Gppp
                                                     │
                                                     ▼
                                             Adicionar 100 A
                                                     │
                                                     ▼
                                                mRNA MADURO
```

---

# ⚠️ Classificações

De acordo com as regras do BioCompiler 2.0, uma sequência pode apresentar os seguintes resultados:

## ✅ CORRETO

Existe uma estrutura válida:

```text
GU ... A ... AG
```

com um branch point válido localizado entre **10 e 30 nucleotídeos antes do AG terminal**.

Nesse caso, o sistema realiza o splicing e gera o mRNA maduro.

---

## ❌ BUG - sítio 5' ausente

Existe um `AG`, mas não existe um `GU` anterior compatível capaz de iniciar o íntron.

```text
AG encontrado
GU anterior compatível ausente
```

Resultado:

```text
BUG - sítio 5' ausente
```

---

## ❌ BUG - sítio 3' ausente

Existe um `GU`, mas não existe um `AG` posterior compatível capaz de finalizar o íntron.

```text
GU encontrado
AG posterior compatível ausente
```

Resultado:

```text
BUG - sítio 3' ausente
```

---

## ❌ BUG - branch point

Existem `GU` e `AG` em posições compatíveis, mas não existe uma adenina válida entre **10 e 30 nucleotídeos antes do AG terminal**.

Resultado:

```text
BUG - branch point
```

---

# ▶️ Como executar o projeto

## 1. Clonar o repositório

```bash
git clone https://github.com/MonnikLuianne/Biocompiler-2.0-do-pre-mRNA-ao-mRNA-maduro.git
```

## 2. Acessar a pasta do projeto

```bash
cd Biocompiler-2.0-do-pre-mRNA-ao-mRNA-maduro
```

## 3. Criar o ambiente virtual

No Windows:

```bash
python -m venv .venv
```

## 4. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

## 5. Instalar as dependências

```bash
pip install -r requirements.txt
```

## 6. Executar o processamento pelo terminal

```bash
python biocompiler.py
```

O sistema realizará o processamento das **40 sequências** presentes no arquivo:

```text
BioCompiler2_entrada_40_casos_modelo_oficial.txt
```

Os resultados serão apresentados no terminal e também será gerado o arquivo:

```text
resultados.txt
```

## 7. Executar a interface gráfica

```bash
streamlit run app.py
```

Após executar o comando, o Streamlit abrirá a aplicação no navegador.

---

# 🖥️ Utilização do sistema

Na interface do BioCompiler 2.0:

1. As 40 sequências do arquivo oficial são carregadas;
2. Clique no botão **Iniciar execução**;
3. O sistema processará cada entrada individualmente;
4. Cada sequência será classificada;
5. O diagnóstico será apresentado;
6. Para as entradas classificadas como `CORRETO`, será apresentado o mRNA maduro;
7. O relatório mostrará a quantidade de entradas corretas e com erros;
8. Os resultados poderão ser exportados através da interface.

---

# 📄 Exportação dos resultados

O BioCompiler gera resultados no seguinte formato:

```text
linha;status;resultado;mRNA_maduro
```

Exemplo de uma entrada correta:

```text
1;OK;CORRETO;m7GpppSEQUÊNCIA_PROCESSADAAAAAAAA...
```

Exemplo de uma entrada com erro:

```text
2;ERRO;BUG - sítio 5' ausente;NÃO GERADO
```

Os campos representam:

- `linha`: número da entrada no arquivo;
- `status`: `OK` ou `ERRO`;
- `resultado`: diagnóstico produzido pelo BioCompiler;
- `mRNA_maduro`: sequência madura gerada ou `NÃO GERADO` quando a entrada apresenta erro.

O arquivo é salvo em codificação UTF-8.

---

# 🧪 Arquivo oficial de testes

O arquivo utilizado nesta versão contém **40 sequências de pré-mRNA**.

Para o conjunto oficial fornecido, o BioCompiler 2.0 apresenta:

```text
CORRETO: 10
BUG - sítio 5' ausente: 10
BUG - branch point: 10
BUG - sítio 3' ausente: 10

TOTAL: 40
```

---

# 🧬 Resumo do processamento

```text
Pré-mRNA
   ↓
Validação das bases
   ↓
Reconhecimento de GU e AG
   ↓
Validação da estrutura do íntron
   ↓
Validação do branch point
   ↓
Splicing
   ↓
CAP 5' (m7Gppp)
   ↓
Cauda poli-A (100 A)
   ↓
mRNA maduro
```

O **BioCompiler 2.0** encerra seu processamento na geração do **mRNA maduro** e não realiza a tradução da sequência em proteína.