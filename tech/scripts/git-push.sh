#!/bin/bash
# git-push.sh — Add, commit e push in un colpo
# Uso: ./tech/scripts/git-push.sh "messaggio di commit"

set -e

if [ -z "$1" ]; then
  echo "Uso: $0 \"messaggio di commit\""
  exit 1
fi

cd "$(git rev-parse --show-toplevel)"

git add -A
git commit -m "$1"
git push
