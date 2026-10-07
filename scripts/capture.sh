#!/usr/bin/env bash
# Records commands, real output and exit status for the later evidence session.
set -uo pipefail
if [ "$#" -lt 2 ]; then echo 'Usage: capture.sh evidence/file.txt command [args...]' >&2; exit 2; fi
output=$1; shift
mkdir -p "$(dirname "$output")"
{ date -u '+UTC %Y-%m-%dT%H:%M:%SZ'; printf '$ '; printf '%q ' "$@"; printf '\n'; "$@"; result=$?; printf '\nExit status: %s\n' "$result"; exit "$result"; } 2>&1 | tee "$output"
exit "${PIPESTATUS[0]}"
