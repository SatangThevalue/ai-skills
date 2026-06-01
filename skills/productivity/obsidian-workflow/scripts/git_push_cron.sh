#!/usr/bin/env bash
# idempotent git push helper used by cron — will commit local changes and push to origin if set
set -euo pipefail
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
# stage
if git diff --quiet && git diff --cached --quiet; then
  echo "No changes"
  exit 0
fi
git add -A
if git diff --cached --quiet; then
  echo "No staged changes"
  exit 0
fi
msg="autocommit: $(date --iso-8601=seconds)"
GIT_COMMITTER_DATE="$(date --iso-8601=seconds)" git commit -m "$msg"
# push if origin exists
if git ls-remote --exit-code origin >/dev/null 2>&1; then
  git push origin "$BRANCH" || true
else
  echo "No origin configured"
fi
