# Transcrição de Consultas Médicas

Projeto acadêmico desenvolvido para a disciplina **Aspectos de IA para Saúde Digital**.

## Objetivo

Experimentar o reconhecimento automático de voz (*Automatic Speech Recognition — ASR*) aplicado a gravações de consultas médicas, utilizando inteligência artificial para gerar transcrições e avaliar sua qualidade.

## Proposta

O projeto utiliza áudios de consultas médicas simuladas e suas respectivas transcrições de referência.

A transcrição automática é realizada com o **OpenAI Whisper**. Os resultados são comparados com as transcrições de referência utilizando a métrica **Word Error Rate (WER)**, que permite avaliar a quantidade de erros na transcrição.

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

Até o momento, os experimentos foram realizados com o dataset do Hugging Face.

Os arquivos do dataset são armazenados localmente, fora do diretório do projeto, em:

`~/PythonFolder/TranscricaoConsultaMedicaDataSets/`

A estrutura local dos dados é:

```text
TranscricaoConsultaMedicaDataSets/
├── audios_fornecidos/
└── transcricoes_fornecidas/
```

Essa organização mantém os áudios e as transcrições de referência separados do código-fonte e evita seu envio acidental ao GitHub.

## Execução

Com o ambiente virtual ativado e as dependências instaladas, execute o pipeline a partir da raiz do projeto:

```bash
python -m src.pipeline
```

O pipeline realiza as seguintes etapas:

1. Localiza os arquivos de áudio disponíveis.
2. Carrega o modelo Whisper uma única vez.
3. Percorre os áudios e localiza suas respectivas transcrições de referência pelo nome do arquivo.
4. Gera a transcrição automática de cada áudio.
5. Compara a transcrição automática com a referência.
6. Salva os resultados individuais e consolida as métricas em um arquivo CSV.
7. Apresenta um resumo geral do processamento.

O modelo utilizado inicialmente é o Whisper `base`.

## Resultados

A avaliação utiliza a métrica Word Error Rate (WER), calculada pela seguinte fórmula:

**WER = (Substituições + Exclusões + Inserções) / Total de palavras da referência**

O relatório CSV contém, para cada consulta:

- Identificação da consulta.
- Quantidade de palavras na referência.
- Quantidade de palavras reconhecidas pelo Whisper.
- Acertos (*hits*).
- Substituições (*substitutions*).
- Exclusões (*deletions*).
- Inserções (*insertions*).
- WER individual.

O WER global é calculado pela soma dos erros de todas as consultas avaliadas dividida pela soma das palavras de referência dessas consultas.

### Primeiro processamento completo

No primeiro processamento dos 272 áudios, foram obtidos os seguintes resultados:

| Indicador | Resultado |
|---|---:|
| Consultas encontradas | 272 |
| Consultas avaliadas | 270 |
| Consultas com erro | 2 |
| Palavras de referência avaliadas | 354.151 |
| Total de erros | 58.218 |
| WER global parcial | 16,44% |

As consultas `RES0002` e `RES0054` apresentaram erros de decodificação UTF-8 durante a leitura das transcrições de referência.

Por esse motivo, o resultado de 16,44% representa somente as 270 consultas avaliadas e ainda não corresponde à avaliação completa do dataset.

## Status

Pipeline de transcrição e avaliação implementado e validado com uma consulta individual e um primeiro processamento do conjunto completo.

Em andamento: investigação e correção da leitura das duas transcrições de referência que apresentaram problemas de codificação, seguida de nova execução para completar a avaliação das 272 consultas.