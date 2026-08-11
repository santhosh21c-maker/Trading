#!/usr/bin/env bash
set -euo pipefail

# Idempotent bootstrap for Pine Script development tooling.
export PATH="${HOME}/.local/bin:${PATH}"

if ! command -v pine-validator >/dev/null 2>&1; then
  pip3 install --user --no-warn-script-location \
    git+https://github.com/Poryaei/pine-script-validator.git
fi

if ! command -v pine-validator >/dev/null 2>&1; then
  echo "pine-validator not found after install; ensure ~/.local/bin is on PATH" >&2
  exit 1
fi

echo "Pine Script validator ready: $(pine-validator --help 2>&1 | head -1)"
