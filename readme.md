# Trabalho de Computação Escalável

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

O script de ingestão `download_data.py` foi implementado com auxílio de IA generativa.
