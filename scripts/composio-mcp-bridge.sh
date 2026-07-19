#!/usr/bin/env bash
set -euo pipefail
export PATH="${HOME}/.composio:${PATH}"
export COMPOSIO_INSTALL_DIR="${HOME}/.composio"
# Prefer Hermes agent venv (has mcp SDK)
PY="${HOME}/.hermes/hermes-agent/venv/bin/python"
if [[ ! -x "$PY" ]]; then
  PY="$(command -v python3)"
fi
exec "$PY" "${HOME}/.hermes/bin/composio-mcp-bridge.py"
