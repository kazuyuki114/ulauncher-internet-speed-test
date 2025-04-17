#!/usr/bin/bash
set -euo pipefail
IFS=$'\n\t'

# Defaults
message=""
branch=""

usage() {
  cat <<EOF
Usage: $0 -m MESSAGE [-b BRANCH]
  -m MESSAGE  Commit message (required)
  -b BRANCH   Branch to create/switch (optional)
EOF
  exit 1
}

# Parse options
while getopts ":m:b:" opt; do
  case $opt in
    m) message="$OPTARG" ;;
    b) branch="$OPTARG" ;;
    *) usage ;;
  esac
done
[[ -z "$message" ]] && usage

# Helpers
log()   { echo "[INFO] $*"; }
error() { echo "[ERROR] $*" >&2; exit 1; }

# Ensure Git repo
git rev-parse --is-inside-work-tree &>/dev/null || error "Not a Git repository"

# Branch logic
if [[ -n "$branch" ]]; then
  if git show-ref --verify --quiet "refs/heads/$branch"; then
    git checkout "$branch"
    log "Switched to branch '$branch'"
  else
    git checkout -b "$branch"
    log "Created & switched to branch '$branch'"
  fi
fi

# Stage, commit, pull then push
git add .
log "Staged all changes"

# Check for changes before committing
if git diff-index --quiet HEAD --; then
    log "No changes detected; skipping commit, pull, and push"
    exit 0
else
    git commit -m "$message"
    log "Committed: $message"
fi

# Pull latest changes
if git pull; then
    log "git pull succeeded"
else
    error "git pull failed; aborting"
    exit 1
fi

current_branch="${branch:-$(git rev-parse --abbrev-ref HEAD)}"

# Push commits
if git push origin "$current_branch"; then
    log "Pushed to '$current_branch'"
else
    error "Git push failed"
    exit 1
fi

log "git-auto completed successfully"
