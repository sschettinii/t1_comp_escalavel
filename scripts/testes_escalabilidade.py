#!/usr/bin/env python3
"""Roda os testes de escalabilidade e salva os tempos em CSV.

Para cada algoritmo e dataset, executa o programa Scala com tamanhos crescentes
de dados (por padrão de 10 mil a 150 mil, de 10 em 10 mil) e grava cada medição
em ``resultados/tempos.csv``.

Contrato com o programa Scala
-----------------------------
O script chama, via sbt::

    runMain <classe> <algoritmo> <dataset> <n>

por exemplo ``runMain Main knn road 10000``. Ao final de cada execução o
programa deve imprimir UMA linha neste formato (é o formato de saída comum aos
dois algoritmos)::

    RESULTADO,<algoritmo>,<dataset>,<n>,<tempo_ms>,<rmse>

O tempo deve medir só o algoritmo, sem a leitura do CSV e sem a inicialização
do Spark, como pedem as instruções do trabalho.

Todas as execuções de um par (algoritmo, dataset) rodam numa única sessão do
sbt, o que evita pagar a inicialização do sbt a cada tamanho.

Este script foi gerado com ajuda de IA generativa (permitido pelas regras do
trabalho para automação dos testes de escalabilidade).
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PREFIXO = "RESULTADO,"
CABECALHO = ("algoritmo", "dataset", "n", "repeticao", "tempo_ms", "rmse", "data_hora")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--algoritmos", nargs="+", default=["knn", "rf"])
    parser.add_argument("--datasets", nargs="+", default=["road", "sgemm"])
    parser.add_argument("--inicio", type=int, default=10_000)
    parser.add_argument("--fim", type=int, default=150_000)
    parser.add_argument("--passo", type=int, default=10_000)
    parser.add_argument(
        "--repeticoes", type=int, default=3,
        help="quantas vezes medir cada tamanho (o gráfico usa a média)",
    )
    parser.add_argument("--classe", default="Main", help="classe com o main do projeto")
    parser.add_argument("--saida", default="resultados/tempos.csv")
    return parser.parse_args()


def localizar_sbt() -> str:
    # No Windows o executável costuma ser sbt.bat; shutil.which resolve os dois casos
    sbt = shutil.which("sbt")
    if sbt is None:
        sys.exit("[erro] sbt não encontrado no PATH.")
    return sbt


def rodar(sbt: str, classe: str, algoritmo: str, dataset: str,
          tamanhos: list[int], repeticoes: int) -> list[list[str]]:
    comandos = [
        f"runMain {classe} {algoritmo} {dataset} {n}"
        for n in tamanhos
        for _ in range(repeticoes)
    ]
    print(f"\n[rodando] {algoritmo} / {dataset}: {len(comandos)} execuções", flush=True)

    processo = subprocess.Popen(
        [sbt, "-batch", *comandos],
        cwd=RAIZ,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    resultados: list[list[str]] = []
    assert processo.stdout is not None
    for linha in processo.stdout:
        # O sbt pode prefixar a saída do programa com "[info] "; procuramos o marcador na linha
        if PREFIXO in linha:
            campos = linha[linha.index(PREFIXO):].strip().split(",")[1:]
            if len(campos) != 5:
                print(f"[aviso] linha de resultado mal formada: {linha.strip()}")
                continue
            resultados.append(campos)
            print(f"  {campos[0]} {campos[1]} n={campos[2]}: {campos[3]} ms, rmse={campos[4]}",
                  flush=True)
        elif "[error]" in linha or "Exception" in linha:
            print("  " + linha.rstrip(), flush=True)

    if processo.wait() != 0:
        print(f"[aviso] o sbt terminou com código {processo.returncode} em {algoritmo}/{dataset}")
    if len(resultados) != len(comandos):
        print(f"[aviso] esperava {len(comandos)} resultados e recebi {len(resultados)}")
    return resultados


def main() -> int:
    args = parse_args()
    sbt = localizar_sbt()
    tamanhos = list(range(args.inicio, args.fim + 1, args.passo))

    saida = RAIZ / args.saida
    saida.parent.mkdir(parents=True, exist_ok=True)
    novo = not saida.exists()

    with saida.open("a", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        if novo:
            escritor.writerow(CABECALHO)

        for algoritmo in args.algoritmos:
            for dataset in args.datasets:
                contagem: dict[str, int] = {}
                for alg, ds, n, tempo_ms, rmse in rodar(
                    sbt, args.classe, algoritmo, dataset, tamanhos, args.repeticoes
                ):
                    contagem[n] = contagem.get(n, 0) + 1
                    agora = datetime.now().isoformat(timespec="seconds")
                    escritor.writerow((alg, ds, n, contagem[n], tempo_ms, rmse, agora))
                arquivo.flush()

    print(f"\n[ok] resultados em {saida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
