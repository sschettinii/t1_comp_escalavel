# Estudos de Scala

Material de estudo da linguagem Scala usado antes da implementação do trabalho. Os exercícios ficam em [`ex_scala.ipynb`](ex_scala.ipynb) e as notas de cada parte em [`notas/`](notas/).

| Parte | Conteúdo | Exercícios |
| --- | --- | --- |
| 1 | `val` e `var`, tipos, interpolação de strings, funções, `if`, `while`, `for`, `Array`, `map`, `filter`, tuplas, `case class` | 1 a 15 |
| 2 | [Funções de ordem superior e reduções](notas/parte-2-ordem-superior-e-reducoes.md): `_`, tipos de função, `foldLeft`, `reduce`, `zip`, `count`, `minBy`, `sortBy` | 16 a 24 |

## Ambiente

O notebook roda no JupyterLab com o kernel **Almond 0.15** para **Scala 2.13.18**, a mesma linha de Scala usada pelo Spark 4. O Java 21 é gerenciado pelo Coursier e não altera o Java padrão do sistema.

Requisitos: macOS ou Linux x86_64, Python 3 e `curl`.

### Iniciar

```bash
cd estudos/scala
./start-jupyter.sh
```

Na primeira execução, o script chama `./setup-jupyter.sh`, que baixa o Coursier, instala o JupyterLab num ambiente virtual local e registra o kernel. Depois disso, o navegador abre o JupyterLab. Para notebooks novos, escolha o kernel **Scala 2.13 (Almond)**.

Para encerrar, pressione `Ctrl+C` no terminal em que o Jupyter está rodando e confirme.

### Diretórios locais

Os diretórios abaixo são gerados pelo ambiente, ficam só na máquina e são ignorados pelo git:

- `.venv/`: JupyterLab;
- `.tools/`: executável do Coursier;
- `.coursier-cache/`: dependências Scala e Almond;
- `.jupyter/`: configuração e especificação do kernel;
- `.ipynb_checkpoints/`: checkpoints automáticos dos notebooks.

## Dicas

- O kernel perde todas as definições quando é reiniciado. Antes de continuar de onde parou, use **Run → Run All Above Selected Cell**.
- Dependências compiladas para Scala 3 não devem ser misturadas com as de Scala 2.13. A sintaxe básica dos dois é parecida, mas o Spark usa Scala 2.13.
