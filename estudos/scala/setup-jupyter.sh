#!/usr/bin/env bash
# Prepara, dentro deste diretório, o JupyterLab com o kernel Scala 2.13 (Almond).
# Coursier, dependências Scala, JupyterLab e kernel ficam em diretórios locais
# ignorados pelo git; o JDK 21 vai para o cache global do Coursier e não altera
# o Java padrão do sistema. Pode ser executado de novo sem problemas.
set -euo pipefail

ALMOND_VERSION="0.15.0"
SCALA_VERSION="2.13.18"   # mesma linha de Scala usada pelo Spark 4
COURSIER_VERSION="2.1.26"
JAVA_VERSION="21"

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$project_dir"

cs_bin="$project_dir/.tools/cs"
kernel_dir="$project_dir/.jupyter/kernels"
export COURSIER_CACHE="$project_dir/.coursier-cache"
export COURSIER_REPOSITORIES="central|https://jitpack.io"

# 1. Coursier: gerenciador de dependências e de JDKs do ecossistema Scala.
if [ ! -x "$cs_bin" ]; then
  case "$(uname -s)-$(uname -m)" in
    Darwin-arm64)  asset="cs-aarch64-apple-darwin.gz" ;;
    Darwin-x86_64) asset="cs-x86_64-apple-darwin.gz" ;;
    Linux-x86_64)  asset="cs-x86_64-pc-linux.gz" ;;
    *) echo "Plataforma não suportada: $(uname -s) $(uname -m)" >&2; exit 1 ;;
  esac
  echo "[setup] baixando Coursier $COURSIER_VERSION"
  mkdir -p "$project_dir/.tools"
  curl -fsSL "https://github.com/coursier/coursier/releases/download/v$COURSIER_VERSION/$asset" \
    | gzip -d > "$cs_bin.tmp"
  chmod +x "$cs_bin.tmp"
  mv "$cs_bin.tmp" "$cs_bin"
fi

# 2. Java 21, gerenciado pelo Coursier, sem alterar o Java padrão do sistema.
echo "[setup] preparando Java $JAVA_VERSION"
export JAVA_HOME="$("$cs_bin" java-home --jvm "$JAVA_VERSION")"
export PATH="$JAVA_HOME/bin:$PATH"

# 3. JupyterLab num ambiente virtual Python local.
if [ ! -x "$project_dir/.venv/bin/jupyter" ]; then
  echo "[setup] criando .venv com JupyterLab"
  python3 -m venv "$project_dir/.venv"
  "$project_dir/.venv/bin/pip" install --quiet --upgrade pip
  "$project_dir/.venv/bin/pip" install --quiet "jupyterlab>=4,<5"
fi

# 4. Kernel Almond para Scala 2.13.
echo "[setup] instalando o kernel Almond $ALMOND_VERSION (Scala $SCALA_VERSION)"
# O launcher do Almond grava --scala no kernel.json; por isso a versão vai depois do "--".
"$cs_bin" launch --use-bootstrap "sh.almond:launcher_3:$ALMOND_VERSION" -- \
  --install --force \
  --scala "$SCALA_VERSION" \
  --id scala213 \
  --display-name "Scala 2.13 (Almond)" \
  --jupyter-path "$kernel_dir" \
  --env "COURSIER_CACHE=$COURSIER_CACHE" \
  --env "COURSIER_REPOSITORIES=$COURSIER_REPOSITORIES"

echo "[ok] ambiente pronto. Rode ./start-jupyter.sh"
