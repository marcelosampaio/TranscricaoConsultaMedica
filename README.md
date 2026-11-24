# Transcrição de Consultas Médicas

Projeto acadêmico desenvolvido para a disciplina **Aspectos de IA para Saúde Digital**.

## Objetivo

Experimentar o reconhecimento automático de voz (*Automatic Speech Recognition — ASR*) aplicado a gravações de consultas médicas, utilizando inteligência artificial para gerar transcrições e avaliar sua qualidade.

## Proposta

O projeto utiliza áudios de consultas médicas simuladas e suas respectivas transcrições de referência.

A transcrição automática é realizada com o **OpenAI Whisper**. Os resultados são comparados com as transcrições de referência utilizando a métrica **Word Error Rate (WER)**, que permite avaliar a quantidade de divergências entre os textos.

O processamento é realizado individualmente para cada consulta, permitindo analisar os resultados e calcular o WER global do conjunto avaliado.

## Tecnologias

- Python 3.11
- OpenAI Whisper
- Jiwer
- PyTorch
- FFmpeg
- Git e GitHub

## Organização do projeto

```text
TranscricaoConsultaMedica/
├── src/
│   ├── transcrever.py
│   ├── avaliar_transcricao.py
│   └── pipeline.py
├── results/
│   ├── transcricoes/
│   └── avaliacao.csv
├── requirements.txt
├── README.md
└── .gitignore
```

- `src/`: código-fonte da aplicação.
- `transcrever.py`: carregamento do modelo Whisper e transcrição dos áudios.
- `avaliar_transcricao.py`: normalização dos textos e cálculo das métricas de avaliação.
- `pipeline.py`: coordenação do processamento das consultas, geração das transcrições e consolidação dos resultados.
- `results/`: armazenamento local dos resultados gerados pelos experimentos.
- `requirements.txt`: dependências Python do projeto.

## Dataset

Os dados utilizados são provenientes do dataset recomendado pelo professor:

- [Hugging Face - Medical Dataset](https://huggingface.co/datasets/yfyeung/medical)

Outra fonte recomendada:

- [Kaggle - Doctor Patient Conversation Large](https://www.kaggle.com/datasets/azmayensabil/doctor-patient-conversation-large)

Os experimentos deste projeto foram realizados com o dataset do Hugging Face.

Os arquivos do dataset são armazenados localmente, fora do diretório do projeto, em:

```text
~/PythonFolder/TranscricaoConsultaMedicaDataSets/
```

A estrutura local esperada é:

```text
TranscricaoConsultaMedicaDataSets/
├── audios_fornecidos/
│   ├── CAR0001.mp3
│   └── ...
└── transcricoes_fornecidas/
    ├── CAR0001.txt
    └── ...
```

Os arquivos de áudio e suas respectivas transcrições devem possuir o mesmo identificador. Por exemplo, `CAR0001.mp3` deve corresponder a `CAR0001.txt`.

Essa organização mantém os áudios e as transcrições de referência separados do código-fonte e evita seu envio acidental ao GitHub.

## Instalação e configuração

### Pré-requisitos

- Python 3.11 instalado.
- Git instalado.
- FFmpeg instalado.
- Dataset preparado conforme a estrutura descrita anteriormente.

No macOS, o FFmpeg pode ser instalado pelo Homebrew:

```bash
brew install ffmpeg
```

### 1. Clonar o repositório

```bash
git clone https://github.com/marcelosampaio/TranscricaoConsultaMedica.git
cd TranscricaoConsultaMedica
```

### 2. Criar o ambiente virtual

```bash
python3.11 -m venv .venv
```

### 3. Ativar o ambiente virtual

No macOS ou Linux:

```bash
source .venv/bin/activate
```

### 4. Instalar as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Preparar o dataset

Obtenha o dataset [Medical Dataset no Hugging Face](https://huggingface.co/datasets/yfyeung/medical) e organize os arquivos localmente nas pastas:

- `audios_fornecidos/`: arquivos de áudio MP3.
- `transcricoes_fornecidas/`: arquivos TXT de referência.

O diretório deve estar localizado em:

```text
~/PythonFolder/TranscricaoConsultaMedicaDataSets/
```

Os arquivos não devem ser colocados dentro do repositório.

## Execução

Com o ambiente virtual ativado, execute o pipeline a partir da raiz do projeto:

```bash
python -m src.pipeline
```

Na primeira execução, o Whisper poderá precisar de acesso à internet para baixar o modelo `base`. Depois que o modelo estiver armazenado localmente, o processamento poderá ser realizado offline, desde que as dependências e os arquivos necessários estejam disponíveis.

O pipeline realiza as seguintes etapas:

1. Localiza os arquivos de áudio disponíveis.
2. Carrega o modelo Whisper uma única vez.
3. Percorre os áudios e localiza suas respectivas transcrições de referência pelo nome do arquivo.
4. Gera a transcrição automática de cada áudio.
5. Compara a transcrição automática com a referência.
6. Salva os resultados individuais e consolida as métricas em um arquivo CSV.
7. Apresenta um resumo geral do processamento, incluindo horários de início e término e duração total.

O modelo utilizado é o Whisper `base`.

No macOS com Apple Silicon, o projeto utiliza o dispositivo MPS quando disponível, permitindo aproveitar a aceleração de processamento da GPU integrada.

## Resultados

A avaliação utiliza a métrica Word Error Rate (WER), calculada pela seguinte fórmula:

**WER = (Substituições + Exclusões + Inserções) / Total de palavras da referência**

A comparação identifica três tipos de divergência:

- **Substituições (*Substitutions*):** uma palavra da referência foi reconhecida como outra.
- **Exclusões (*Deletions*):** uma palavra da referência não apareceu na transcrição automática.
- **Inserções (*Insertions*):** uma palavra foi acrescentada na transcrição automática sem correspondência na referência.

O relatório CSV contém, para cada consulta:

- Identificação da consulta.
- Quantidade de palavras na referência.
- Quantidade de palavras reconhecidas pelo Whisper.
- Acertos (*hits*).
- Substituições (*substitutions*).
- Exclusões (*deletions*).
- Inserções (*insertions*).
- WER individual.

O WER global é calculado pela soma das substituições, exclusões e inserções de todas as consultas avaliadas, dividida pela soma das palavras de referência dessas consultas.

Os resultados são armazenados localmente em:

```text
results/
├── transcricoes/
│   ├── CAR0001.txt
│   ├── ...
└── avaliacao.csv
```

## Resultado do processamento completo

Em 23/11/2026, foi realizado o processamento completo do conjunto de dados, contemplando as 272 consultas disponíveis.

| Indicador | Resultado |
|---|---:|
| Consultas encontradas | 272 |
| Consultas avaliadas | 272 |
| Consultas com erro | 0 |
| Palavras na referência | 357.519 |
| Total de operações de erro | 58.702 |
| WER global | 16,42% |
| Tempo de processamento | 02:22:10 |

**Horário de execução:**

- Início: 23/11/2026 às 16:12:22.
- Término: 23/11/2026 às 18:34:30.
- Duração total: 2 horas, 22 minutos e 10 segundos.

O processamento foi concluído sem falhas, contemplando 100% das consultas disponíveis no dataset.

O WER global de 16,42% representa a proporção de operações de divergência textual em relação ao total de palavras das transcrições de referência. Essa métrica não identifica isoladamente a causa das divergências, que podem estar relacionadas, entre outros fatores, à qualidade do áudio, à sobreposição de vozes e às características da fala espontânea.

## Status

Pipeline de transcrição e avaliação implementado e validado.

O processamento completo das 272 consultas foi concluído com sucesso, sem falhas de processamento, e os resultados foram consolidados em arquivos TXT individuais e relatório CSV.

O projeto permite reproduzir localmente o experimento de reconhecimento automático de voz e avaliação das transcrições utilizando o modelo Whisper `base`.