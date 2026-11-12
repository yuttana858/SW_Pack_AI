#!/usr/bin/env bash
# Run a Modal CLI command in CI with the deploy token cleaned and checked first.
# Usage: deploy/ci_modal.sh <modal arguments...>      e.g. deploy/ci_modal.sh deploy deploy/modal_app.py
# Never prints the token values.
set -euo pipefail
MODAL_TOKEN_ID="$(printf '%s' "${MODAL_TOKEN_ID:-}" | tr -d '[:space:]')"
MODAL_TOKEN_SECRET="$(printf '%s' "${MODAL_TOKEN_SECRET:-}" | tr -d '[:space:]')"
export MODAL_TOKEN_ID MODAL_TOKEN_SECRET
fail() { echo "::error title=Modal deploy token::$1"; exit 1; }
[ -n "$MODAL_TOKEN_ID" ] || fail "Repository secret MODAL_TOKEN_ID is missing (Settings > Secrets and variables > Actions)."
[ -n "$MODAL_TOKEN_SECRET" ] || fail "Repository secret MODAL_TOKEN_SECRET is missing (Settings > Secrets and variables > Actions)."
case "$MODAL_TOKEN_ID" in
  wk-*) fail "MODAL_TOKEN_ID is a PROXY token (wk-...), e.g. 'SWIS AI'. Deploying needs an API token: Modal > Settings > API Tokens > New token (ak-... / as-...)." ;;
  as-*) fail "MODAL_TOKEN_ID holds the token SECRET (as-...). Put the token ID (ak-...) in MODAL_TOKEN_ID and the secret (as-...) in MODAL_TOKEN_SECRET." ;;
  ak-*) ;;
  *) fail "MODAL_TOKEN_ID should start with ak- (an API token id from Modal > Settings > API Tokens)." ;;
esac
case "$MODAL_TOKEN_SECRET" in
  ws-*) fail "MODAL_TOKEN_SECRET is a PROXY token secret (ws-...). Use the API token secret (as-...)." ;;
  as-*) ;;
  *) fail "MODAL_TOKEN_SECRET should start with as- (the API token secret shown once when the token is created)." ;;
esac
exec modal "$@"
