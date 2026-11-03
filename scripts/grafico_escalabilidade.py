#!/usr/bin/env python3
"""Gera os gráficos de escalabilidade a partir de ``resultados/tempos.csv``.

Um gráfico por dataset, com o tamanho do dataset no eixo X, o tempo de execução
no eixo Y e uma linha para cada algoritmo (média das repetições, com a faixa
entre o menor e o maior tempo medido).

Uso:
    python3 scripts/grafico_escalabilidade.py

Este script foi gerado com ajuda de IA generativa (permitido pelas regras do
trabalho para a produção dos gráficos dos resultados finais).
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

RAIZ = Path(__file__).resolve().parent.parent

NOMES_ALGORITMOS = {"knn": "KNN", "rf": "Random Forest"}
NOMES_DATASETS = {"road": "3D Road Network", "sgemm": "SGEMM GPU Kernel Performance"}
CORES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
MARCADORES = ["o", "s", "^", "D"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera os gráficos de escalabilidade.")
    parser.add_argument("--entrada", default="resultados/tempos.csv")
    parser.add_argument("--pasta", default="resultados")
    parser.add_argument(
        "--segundos", action="store_true", help="mostra o eixo Y em segundos em vez de ms"
    )
    return parser.parse_args()


def carregar(caminho: Path) -> dict[str, dict[str, dict[int, list[float]]]]:
    # dados[dataset][algoritmo][n] = lista de tempos (ms)
    dados: dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        for linha in csv.DictReader(arquivo):
            dados[linha["dataset"]][linha["algoritmo"]][int(linha["n"])].append(
                float(linha["tempo_ms"])
            )
    return dados


def main() -> int:
    args = parse_args()
    dados = carregar(RAIZ / args.entrada)
    pasta = RAIZ / args.pasta
    pasta.mkdir(parents=True, exist_ok=True)
    divisor, unidade = (1000.0, "s") if args.segundos else (1.0, "ms")

    # A cor de cada algoritmo é fixa, então KNN e RF ficam iguais em todos os gráficos
    algoritmos = sorted({alg for por_alg in dados.values() for alg in por_alg})
    estilo = {
        alg: (CORES[i % len(CORES)], MARCADORES[i % len(MARCADORES)])
        for i, alg in enumerate(algoritmos)
    }

    for dataset, por_algoritmo in sorted(dados.items()):
        fig, ax = plt.subplots(figsize=(7, 4.2), dpi=150)

        for algoritmo in algoritmos:
            if algoritmo not in por_algoritmo:
                continue
            medidas = por_algoritmo[algoritmo]
            ns = sorted(medidas)
            medias = [sum(medidas[n]) / len(medidas[n]) / divisor for n in ns]
            minimos = [min(medidas[n]) / divisor for n in ns]
            maximos = [max(medidas[n]) / divisor for n in ns]
            cor, marcador = estilo[algoritmo]

            ax.fill_between(ns, minimos, maximos, color=cor, alpha=0.15, linewidth=0)
            ax.plot(ns, medias, color=cor, linewidth=2, marker=marcador, markersize=5,
                    label=NOMES_ALGORITMOS.get(algoritmo, algoritmo))

        ax.set_title(NOMES_DATASETS.get(dataset, dataset), loc="left", fontsize=12)
        ax.set_xlabel("Tamanho do dataset (pontos)")
        ax.set_ylabel(f"Tempo de execução ({unidade})")
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:.0f} mil"))
        ax.set_ylim(bottom=0)
        ax.grid(axis="y", color="#e2e1dc", linewidth=0.8)
        ax.set_axisbelow(True)
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            ax.spines[lado].set_color("#8a8980")
        ax.legend(frameon=False)
        fig.tight_layout()

        destino = pasta / f"grafico_{dataset}.png"
        fig.savefig(destino)
        plt.close(fig)
        print(f"[ok] {destino}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
