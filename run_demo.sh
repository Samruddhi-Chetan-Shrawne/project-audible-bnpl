#!/usr/bin/env bash
# run_demo.sh - one-command cold start for Project Audible (BNPL vs credit card stress).
#
# Builds a clean virtual environment, runs the whole pipeline in order, rebuilds the
# dashboard data model, and prints where to open the dashboard. No manual steps.
#
# Usage:
#   ./run_demo.sh            full run: pulls FRED + SEC EDGAR live, then parses and rebuilds
#   ./run_demo.sh --offline  skips the two live pulls and the filing parse; rebuilds the
#                            chart, lag table and dashboard from the committed
#                            data/processed/*.csv (use if SEC or FRED is unreachable)
#
# Needs: Python 3.11+ on PATH (override with PYTHON=/path/to/python), internet for pip.
# On Windows run it from Git Bash or WSL.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

OFFLINE=0
[[ "${1:-}" == "--offline" ]] && OFFLINE=1

# Find a Python 3.11+ interpreter. Windows (Git Bash) usually has `python` or `py`, not `python3`.
if [[ -z "${PYTHON:-}" ]]; then
  for candidate in python3 python py; do
    if command -v "$candidate" >/dev/null 2>&1 \
       && "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
      PYTHON="$candidate"
      break
    fi
  done
fi
PYTHON="${PYTHON:-python3}"
if ! "$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
  echo "ERROR: Python 3.11+ is required (found: $("$PYTHON" --version 2>&1 || echo none))." >&2
  echo "Set PYTHON=/path/to/python3.11+ and re-run." >&2
  exit 1
fi

echo "==> [1/3] Creating clean environment (.venv)"
rm -rf .venv
"$PYTHON" -m venv .venv
# shellcheck disable=SC1091
if [[ -f .venv/bin/activate ]]; then source .venv/bin/activate; else source .venv/Scripts/activate; fi
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

echo "==> [2/3] Running pipeline"
if [[ $OFFLINE -eq 0 ]]; then
  python scripts/pull_fred.py
  python scripts/fetch_affirm_filings.py
  python scripts/parse_affirm_delinquency.py
else
  echo "    (--offline) skipping live pulls; using committed data/processed/*.csv"
fi
python scripts/chart_lead_lag.py
python scripts/lead_lag.py
python scripts/build_dashboard_data.py

echo "==> [3/3] Done"
echo "Open this file in a browser (it runs offline, Plotly is vendored):"
echo "    $(pwd)/dashboard/index.html"
echo "Headline chart: $(pwd)/outputs/chart_lead_lag.png"
