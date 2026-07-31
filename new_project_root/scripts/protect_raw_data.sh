#!/usr/bin/env bash
# Refuse commits that alter existing originals under the raw data directory.
#
# Allowed: adding new raw data, and reorganising it. Git reports a pure rename
# as R100, which cannot change a single byte, so directory curation is fine.
# Refused: modifying, retyping or deleting a committed original, and renaming
# it with edits (similarity below 100). Override a deliberate exception:
#   GA_ALLOW_RAW=1 git commit -m "..."
set -euo pipefail

RAW_DIR="${GA_RAW_DIR:-data/raw}"

if [ "${GA_ALLOW_RAW:-0}" = "1" ]; then
    exit 0
fi

# Modification, typechange and deletion always alter or remove an original.
altered=$(git diff --cached --name-only --diff-filter=MTD -- "$RAW_DIR")

# Renames print "R<similarity>\told\tnew"; below R100 they carry content edits,
# so treat those exactly like a modification and report the destination path.
edited_renames=$(git diff --cached --name-status --diff-filter=R -- "$RAW_DIR" |
    awk '$1 != "R100" { print $3 }')

blocked=$(printf '%s\n%s\n' "$altered" "$edited_renames" | grep -v '^$' || true)

if [ -n "$blocked" ]; then
    echo "ERROR: existing files altered in '$RAW_DIR/' (immutable raw data policy)." >&2
    echo "Blocked files:" >&2
    echo "$blocked" >&2
    echo >&2
    echo "If this is intentional, commit with override:" >&2
    echo "  GA_ALLOW_RAW=1 git commit -m \"...\"" >&2
    exit 1
fi
