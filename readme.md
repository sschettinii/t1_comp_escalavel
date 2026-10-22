# Trabalho de Computação Escalável

## Documentação do trabalho

As [instruções do trabalho do semestre](docs/trabalho-semestre/README.md) reúnem os requisitos, o cronograma, as regras de uso de IA e os materiais originais fornecidos pela professora.

## Ingestão dos dados

Com o Python 3 instalado, execute na raiz do repositório:

```bash
python3 download_data.py
```

Os datasets serão baixados e preparados no diretório `data/`.

## Datasets e regressão

- **3D Road Network:** utiliza longitude e latitude para prever a altitude de pontos de uma malha rodoviária.
- **SGEMM GPU Kernel Performance:** utiliza 14 configurações de execução para prever o tempo médio de processamento de uma multiplicação de matrizes.

Os algoritmos Random Forest e KNN serão implementados para regressão e comparados quanto ao tempo de execução e à escalabilidade conforme o volume de dados aumenta.

## Uso de IA generativa

Foi utilizada IA generativa para:

- implementar a ingestão inicial dos arquivos em `download_data.py`;
- organizar e transcrever as instruções da professora em `docs/trabalho-semestre/README.md`.

Não foi utilizada IA generativa na implementação dos algoritmos paralelos ou distribuídos.
