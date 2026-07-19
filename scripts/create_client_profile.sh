#!/usr/bin/env bash
# Create a Hermes client profile from this template.
set -euo pipefail
NAME="${1:-}"
TRADE="${2:-plumbing}"  # plumbing | trade-frontdesk
if [[ -z "$NAME" ]]; then
  echo "Usage: $0 <profile-name> [plumbing|trade-frontdesk]"
  echo "Example: $0 acme-plumbing plumbing"
  exit 1
fi
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/profiles/$TRADE"
if [[ ! -d "$SRC" ]]; then
  echo "Unknown trade template: $TRADE (have: plumbing, trade-frontdesk)"
  exit 1
fi

# Prefer Hermes CLI clone from default if available
if hermes profile list 2>/dev/null | grep -q default; then
  if hermes profile list 2>/dev/null | grep -qw "$NAME"; then
    echo "Profile '$NAME' already exists."
  else
    echo "Creating profile via: hermes profile create $NAME --clone"
    hermes profile create "$NAME" --clone || hermes profile create "$NAME"
  fi
else
  echo "Hermes CLI not ready; creating folder only under ~/.hermes/profiles/$NAME"
  mkdir -p "$HOME/.hermes/profiles/$NAME"
fi

DEST="$HOME/.hermes/profiles/$NAME"
mkdir -p "$DEST"
cp -n "$SRC/SOUL.md" "$DEST/SOUL.md" 2>/dev/null || cp "$SRC/SOUL.md" "$DEST/SOUL.md"
cp -n "$SRC/profile.yaml" "$DEST/profile.yaml" 2>/dev/null || cp "$SRC/profile.yaml" "$DEST/profile.yaml"
if [[ ! -f "$DEST/.env" ]]; then
  cp "$SRC/.env.example" "$DEST/.env"
  echo "Wrote $DEST/.env — fill TELEGRAM_BOT_TOKEN and ALLOWED_USERS"
else
  echo "Keeping existing $DEST/.env"
fi

echo
echo "Next:"
echo "  1) Edit secrets:  nano $DEST/.env"
echo "  2) Start gateway: hermes -p $NAME gateway install --force --start-now --start-on-login"
echo "  3) Check:         hermes -p $NAME gateway status"
