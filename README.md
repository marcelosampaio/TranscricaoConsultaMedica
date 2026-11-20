# Transcrição de Consultas Médicas

Projeto acadêmico desenvolvido para a disciplina Aspectos de IA para Saúde Digital.

## Objetivo

Experimentar o reconhecimento automático de voz (ASR) aplicado a gravações de consultas médicas, utilizando inteligência artificial para gerar transcrições e avaliar sua qualidade.

## Proposta

O projeto utilizará áudios e transcrições de referência fornecidos pelo professor.

A transcrição automática será realizada com o Whisper, e os resultados serão comparados com as transcrições de referência utilizando a métrica Word Error Rate (WER).

## Tecnologias

- Python
- OpenAI Whisper
- Jiwer
- Git e GitHub

## Organização

- `src/`: código-fonte da aplicação.
- `results/`: resultados gerados pelos experimentos.
- `requirements.txt`: dependências Python do projeto.
- `README.md`: documentação do projeto.

## Dataset

Os dados utilizados são provenientes das fontes recomendadas pelo professor:

- [Hugging Face - Medical Dataset](https://huggingface.co/datasets/yfyeung/medical)
- [Kaggle - Doctor Patient Conversation Large](https://www.kaggle.com/datasets/azmayensabil/doctor-patient-conversation-large)

Os arquivos do dataset são armazenados localmente, fora do diretório do projeto, em:

`~/PythonFolder/TranscricaoConsultaMedicaDataSets/`

Essa organização mantém os áudios e as transcrições de referência separados do código-fonte e evita seu envio acidental ao GitHub.

## Status

Configuração inicial do projeto.
