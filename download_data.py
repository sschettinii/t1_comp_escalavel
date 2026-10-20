#!/usr/bin/env python3
"""Baixa e prepara os datasets de regressão usados no projeto.

Os arquivos gerados ficam em ``data/``, na raiz do repositório. O script usa
somente a biblioteca padrão do Python e é idempotente: um arquivo final que
tenha o cabeçalho e o número de registros esperados não é baixado novamente.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Callable, Iterable, TextIO


REPOSITORY_ROOT = Path(__file__).resolve().parent
DATA_DIR = REPOSITORY_ROOT / "data"

ROAD_NETWORK_URL = (
    "https://archive.ics.uci.edu/static/public/246/"
    "3d+road+network+north+jutland+denmark.zip"
)
SGEMM_URL = (
    "https://archive.ics.uci.edu/static/public/440/"
    "sgemm+gpu+kernel+performance.zip"
)

ROAD_NETWORK_HEADER = ("longitude", "latitude", "target")
SGEMM_FEATURES = (
    "MWG",
    "NWG",
    "KWG",
    "MDIMC",
    "NDIMC",
    "MDIMA",
    "NDIMB",
    "KWI",
    "VWM",
    "VWN",
    "STRM",
    "STRN",
    "SA",
    "SB",
)
SGEMM_HEADER = (*SGEMM_FEATURES, "target")


def download(url: str, destination: Path) -> None:
    """Baixa ``url`` para ``destination`` sem carregar o arquivo na memória."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "t1-comp-escalavel-data-ingestion/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            with destination.open("wb") as output:
                shutil.copyfileobj(response, output, length=1024 * 1024)
    except urllib.error.URLError as error:
        raise RuntimeError(f"Falha ao baixar {url}: {error}") from error


def archive_member(archive: zipfile.ZipFile, filename: str) -> str:
    """Localiza um arquivo pelo nome, ignorando metadados do macOS."""
    candidates = [
        name
        for name in archive.namelist()
        if not name.startswith("__MACOSX/") and Path(name).name == filename
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            f"Esperava encontrar uma vez {filename!r} no arquivo, "
            f"mas encontrei {len(candidates)}."
        )
    return candidates[0]


def format_number(value: str) -> str:
    """Valida e serializa um número sem perda relevante de precisão."""
    return format(float(value.strip()), ".15g")


def clean_road_network(source: TextIO, output: TextIO) -> int:
    """Remove o identificador OSM e mantém longitude, latitude e altitude."""
    reader = csv.reader(source)
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(ROAD_NETWORK_HEADER)

    row_count = 0
    for line_number, row in enumerate(reader, start=1):
        if not row or all(not value.strip() for value in row):
            continue
        if len(row) != 4:
            raise ValueError(
                f"Linha {line_number} do 3D Road Network tem {len(row)} "
                "colunas; eram esperadas 4."
            )
        _, longitude, latitude, altitude = row
        writer.writerow(
            (
                format_number(longitude),
                format_number(latitude),
                format_number(altitude),
            )
        )
        row_count += 1
    return row_count


def clean_sgemm(source: TextIO, output: TextIO) -> int:
    """Mantém os 14 parâmetros e usa a média dos quatro tempos como alvo."""
    reader = csv.reader(source)
    raw_header = next(reader, None)
    if raw_header is None:
        raise ValueError("O CSV do SGEMM está vazio.")

    normalized_header = tuple(column.strip() for column in raw_header)
    if normalized_header[: len(SGEMM_FEATURES)] != SGEMM_FEATURES:
        raise ValueError(
            "Cabeçalho inesperado no SGEMM: " + ", ".join(normalized_header)
        )
    if len(normalized_header) != 18:
        raise ValueError(
            f"O SGEMM tem {len(normalized_header)} colunas; eram esperadas 18."
        )

    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(SGEMM_HEADER)

    row_count = 0
    for line_number, row in enumerate(reader, start=2):
        if not row or all(not value.strip() for value in row):
            continue
        if len(row) != 18:
            raise ValueError(
                f"Linha {line_number} do SGEMM tem {len(row)} colunas; "
                "eram esperadas 18."
            )

        features = [format_number(value) for value in row[:14]]
        run_times = [float(value.strip()) for value in row[14:18]]
        target = sum(run_times) / len(run_times)
        writer.writerow((*features, format(target, ".15g")))
        row_count += 1
    return row_count


def valid_output(path: Path, header: Iterable[str], expected_rows: int) -> bool:
    """Confere cabeçalho e quantidade de registros de uma saída existente."""
    if not path.is_file():
        return False

    try:
        with path.open("r", encoding="utf-8", newline="") as source:
            reader = csv.reader(source)
            if tuple(next(reader, ())) != tuple(header):
                return False
            return sum(1 for row in reader if row) == expected_rows
    except (OSError, UnicodeError, csv.Error):
        return False


def build_dataset(
    *,
    name: str,
    url: str,
    archive_filename: str,
    output_filename: str,
    header: Iterable[str],
    expected_rows: int,
    cleaner: Callable[[TextIO, TextIO], int],
    force: bool,
) -> None:
    """Baixa, limpa, valida e publica um dataset de forma atômica."""
    destination = DATA_DIR / output_filename
    if not force and valid_output(destination, header, expected_rows):
        print(f"[ok] {name}: {destination} já está pronto.")
        return

    print(f"[download] {name}")
    with tempfile.TemporaryDirectory(prefix="dataset-", dir=DATA_DIR) as temp_dir:
        temp_root = Path(temp_dir)
        archive_path = temp_root / "source.zip"
        temporary_output = temp_root / output_filename
        download(url, archive_path)

        try:
            with zipfile.ZipFile(archive_path) as archive:
                member = archive_member(archive, archive_filename)
                with archive.open(member) as raw_source:
                    import io

                    with io.TextIOWrapper(
                        raw_source, encoding="utf-8-sig", newline=""
                    ) as source:
                        with temporary_output.open(
                            "w", encoding="utf-8", newline=""
                        ) as output:
                            actual_rows = cleaner(source, output)
        except zipfile.BadZipFile as error:
            raise RuntimeError(f"Download inválido para {name}: não é um ZIP.") from error

        if actual_rows != expected_rows:
            raise RuntimeError(
                f"{name}: foram processados {actual_rows} registros, "
                f"mas eram esperados {expected_rows}."
            )

        temporary_output.replace(destination)
        print(f"[ok] {name}: {actual_rows} registros salvos em {destination}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Baixa e prepara os dois datasets de regressão do projeto."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="baixa e recria os CSVs mesmo que as saídas atuais sejam válidas",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    try:
        build_dataset(
            name="3D Road Network",
            url=ROAD_NETWORK_URL,
            archive_filename="3D_spatial_network.txt",
            output_filename="road_network_3d.csv",
            header=ROAD_NETWORK_HEADER,
            expected_rows=434_874,
            cleaner=clean_road_network,
            force=args.force,
        )
        build_dataset(
            name="SGEMM GPU Kernel Performance",
            url=SGEMM_URL,
            archive_filename="sgemm_product.csv",
            output_filename="sgemm_gpu.csv",
            header=SGEMM_HEADER,
            expected_rows=241_600,
            cleaner=clean_sgemm,
            force=args.force,
        )
    except (OSError, RuntimeError, ValueError, csv.Error) as error:
        print(f"[erro] {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
