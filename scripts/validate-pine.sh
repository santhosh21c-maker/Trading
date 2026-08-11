#!/usr/bin/env bash
set -euo pipefail

export PATH="${HOME}/.local/bin:${PATH}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PINE_FILE="${ROOT}/Smart_Robotic_Logic_Decider_Targets.pine"

if [[ ! -f "${PINE_FILE}" ]]; then
  echo "Missing Pine Script file: ${PINE_FILE}" >&2
  exit 1
fi

echo "==> Static analysis (pine-validator)"
set +e
pine-validator "${PINE_FILE}" --no-hints --no-information 2>&1
validator_status=$?
set -e
if [[ ${validator_status} -ne 0 ]]; then
  echo "pine-validator reported errors (exit ${validator_status})" >&2
  exit "${validator_status}"
fi

echo "==> Ladder math sanity check"
python3 "${ROOT}/scripts/verify-ladder-math.py"

echo "All checks passed."
