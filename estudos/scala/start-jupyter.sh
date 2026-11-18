#!/usr/bin/env bash
# Abre o JupyterLab deste diretório com o kernel Scala 2.13 (Almond).
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cs_bin="$project_dir/.tools/cs"

if [ ! -x "$cs_bin" ] || [ ! -x "$project_dir/.venv/bin/jupyter" ] \
  || [ ! -f "$project_dir/.jupyter/kernels/scala213/kernel.json" ]; then
  "$project_dir/setup-jupyter.sh"
fi

export COURSIER_CACHE="$project_dir/.coursier-cache"
export COURSIER_REPOSITORIES="central|https://jitpack.io"

export JAVA_HOME="$("$cs_bin" java-home --jvm 21 2>/dev/null)"
export PATH="$JAVA_HOME/bin:$PATH"

export JUPYTER_CONFIG_DIR="$project_dir/.jupyter/config"
export JUPYTER_DATA_DIR="$project_dir/.jupyter"
export JUPYTER_RUNTIME_DIR="$project_dir/.jupyter/runtime"

mkdir -p "$JUPYTER_CONFIG_DIR" "$JUPYTER_RUNTIME_DIR"
cd "$project_dir"

exec "$project_dir/.venv/bin/jupyter" lab "$@"
