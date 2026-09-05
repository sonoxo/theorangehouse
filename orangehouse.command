#!/bin/sh
set -eu

cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN=python
else
  echo "Orange House needs Python 3.11 or newer. Install it from https://www.python.org/downloads/" >&2
  exit 1
fi

"$PYTHON_BIN" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)' || {
  echo "Orange House needs Python 3.11 or newer." >&2
  exit 1
}

case "${1:-serve}" in
  test)
    shift
    exec "$PYTHON_BIN" -m unittest discover -s tests -v "$@"
    ;;
  serve|project)
    exec "$PYTHON_BIN" -m orangehouse "$@"
    ;;
  *)
    echo "Usage: ./orangehouse.command [serve|project|test] [options]" >&2
    exit 2
    ;;
esac
