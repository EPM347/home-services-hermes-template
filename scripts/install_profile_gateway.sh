#!/usr/bin/env bash
set -euo pipefail
NAME="${1:-}"
[[ -n "$NAME" ]] || { echo "Usage: $0 <profile-name>"; exit 1; }
hermes -p "$NAME" gateway install --force --start-now --start-on-login
hermes -p "$NAME" gateway status
hermes profile list
