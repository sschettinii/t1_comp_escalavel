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

## Testes de escalabilidade

Com o sbt e o Python 3 (com `matplotlib`) instalados, execute na raiz do repositório:

```bash
python3 scripts/testes_escalabilidade.py
python3 scripts/grafico_escalabilidade.py --segundos
```

O primeiro script roda cada algoritmo em cada dataset com 10 mil a 150 mil pontos, em passos de 10 mil, e salva os tempos em `resultados/tempos.csv`. O segundo gera um gráfico por dataset em `resultados/`, com uma linha para cada algoritmo. Use `--help` para ver as opções, como `--algoritmos knn` para rodar só um deles.

Os dois algoritmos são chamados pela mesma interface, `runMain Main <algoritmo> <dataset> <n>` (algoritmo `knn` ou `rf`, dataset `road` ou `sgemm`), e terminam imprimindo uma linha no formato de saída comum:

```
RESULTADO,<algoritmo>,<dataset>,<n>,<tempo_ms>,<rmse>
```

O tempo medido não inclui a leitura do CSV nem a inicialização do Spark.

## Uso de IA generativa

Foi utilizada IA generativa para:

- implementar a ingestão inicial dos arquivos em `download_data.py`;
- implementar a leitura inicial dos CSVs em `src/main/scala/Dados.scala`;
- implementar a automação dos testes de escalabilidade em `scripts/testes_escalabilidade.py`;
- implementar a geração dos gráficos em `scripts/grafico_escalabilidade.py`;
- organizar e transcrever as instruções da professora em `docs/trabalho-semestre/README.md`.

Não foi utilizada IA generativa na implementação dos algoritmos paralelos ou distribuídos.
