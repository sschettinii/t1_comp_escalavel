# Instruções do trabalho do semestre

Este diretório concentra as instruções apresentadas pela professora nos slides 33 a 39 da aula 8 e os arquivos fornecidos para a entrega do trabalho. Em caso de divergência, os materiais originais da professora são a fonte de verdade.

## Objetivo

Implementar dois algoritmos de mineração ou processamento de dados em ambiente paralelo ou distribuído e analisar a escalabilidade das soluções conforme o volume de dados aumenta.

## Requisitos do projeto

- Escolher uma tarefa de Ciência de Dados, como clustering, classificação, regressão ou associação.
- Implementar dois algoritmos diferentes para a tarefa escolhida.
- Dividir a implementação de modo que cada dupla fique responsável por um algoritmo.
- Usar Java, com Threads, `ExecutorService` e Fork/Join, ou Scala sobre Apache Spark.
- Usar a mesma linguagem nos dois algoritmos.
- Executar os dois algoritmos por meio da mesma interface e gerar o mesmo formato de saída.
- Usar dois datasets distintos, reais ou sintéticos. Se forem sintéticos, empregar distribuições diferentes.
- Avaliar volumes entre 10.000 e 150.000 pontos, ou pelo menos na ordem de 100 mil pontos.
- Manter no GitHub os códigos-fonte, os scripts de execução dos testes e instruções claras para compilar e executar o projeto.

### Exceção para o grupo de três pessoas

O grupo de três deve escolher um algoritmo e implementá-lo com duas decomposições diferentes de dados ou tarefas. As duas versões também devem usar a mesma interface de execução e o mesmo formato de saída.

## Temas sugeridos

- Clustering: k-means e DBSCAN.
- Clustering: hierárquico e k-medoids.
- Regras de associação: Apriori e FP-Growth.
- Busca k-NN: LSH e k-NN por força bruta, com particionamento eficiente.
- Mineração de texto: TF-IDF e CountVectorizer.
- Aprendizado supervisionado: Random Forest, sugestão destinada ao grupo de três pessoas.

Outras propostas são permitidas, mas dois grupos não podem escolher a mesma combinação de algoritmos. A confirmação ocorre por ordem de registro.

## Testes de escalabilidade

Para cada dataset:

1. Aumentar gradualmente o número de pontos, por exemplo em passos de 10 mil.
2. Medir o tempo de execução em cada tamanho.
3. Não incluir na medição inicializações externas ao programa implementado, como a leitura inicial ou a inicialização do framework.
4. Gerar um gráfico com o tamanho do dataset no eixo X e o tempo de execução no eixo Y.
5. Incluir no gráfico duas linhas, uma para cada algoritmo.

## Entregas

| Data | Entrega |
| --- | --- |
| Até 25/10 | Formulário inicial no Google Classroom com integrantes, tarefa, algoritmos, divisão das duplas e link do repositório. |
| Até 12/11 | Relatório final conforme o template fornecido. |
| 13/11 | Apresentação final de aproximadamente 20 minutos por grupo. |
| 27/11 | P2. |

O relatório final deve explicar os algoritmos e as decisões de paralelismo ou distribuição, descrever os experimentos e os resultados de escalabilidade e discutir resultados, melhorias e trabalhos futuros.

## Uso de IA

- Não é permitido usar IA para implementar os algoritmos paralelos ou distribuídos.
- É permitido usar IA para implementar as funções de leitura inicial dos arquivos - e somente essa parte da implementação -, para gerar scripts de automação dos testes de escalabilidade e para produzir os gráficos dos resultados finais.
- O README e o relatório devem declarar se houve uso de IA, para quais finalidades e em quais arquivos.
- O uso será verificado a partir do repositório da equipe.

## Materiais originais

- [Slides da aula 8](materiais-professora/aula8-0910.pdf) - as instruções estão nos slides 33 a 39.
- [Template do relatório final](materiais-professora/template_trabalho_semestre.tex).
- [Logo da UEL usado pelo template](materiais-professora/logo_uel.png).
