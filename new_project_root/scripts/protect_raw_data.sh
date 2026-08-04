#!/usr/bin/env bash
# Refuse commits that alter existing originals under the raw data directory,
# or that add new originals in a mutable (unlocked) form.
#
# Allowed: adding new raw data as locked originals, and reorganising it. Git
# reports a pure rename as R100, which cannot change a single byte, so directory
# curation is fine.
# Refused: modifying, retyping or deleting a committed original, renaming it
# with edits (similarity below 100), and adding an unlocked original.
# Override a deliberate exception:
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

# New originals are welcome, but only locked ones. An unlocked annexed file is
# a mode-100644 pointer whose blob starts with /annex/; it stays writable in the
# worktree, and under annex.thin it is a hardlink to the object, so an in-place
# edit rewrites the only copy. Two routine ingests produce them: `git add`, and
# `git annex add` run from inside the directory -- annex.addunlocked is matched
# against a path relative to the current directory, which then no longer starts
# with the raw directory, so the policy silently misses.
unlocked_adds=""
while IFS= read -r -d '' path; do
    [ "$(git ls-files --stage -- "$path" | awk '{print $1}')" = "100644" ] || continue
    # Pointers are tiny; bail out before reading a real file into memory.
    [ "$(git cat-file -s ":$path" 2>/dev/null || echo 0)" -le 1024 ] || continue
    case "$(git cat-file blob ":$path" 2>/dev/null || true)" in
    /annex/*) unlocked_adds="${unlocked_adds}${path}"$'\n' ;;
    esac
done < <(git diff --cached --name-only --diff-filter=A -z -- "$RAW_DIR")

if [ -n "$unlocked_adds" ]; then
    echo "ERROR: unlocked originals added to '$RAW_DIR/' (immutable raw data policy)." >&2
    echo "Unlocked files:" >&2
    printf '%s' "$unlocked_adds" >&2
    echo >&2
    # `git annex lock` stages the conversion itself. Do not follow it with
    # `git add`: on anything it did not convert, the clean filter stages a fresh
    # unlocked pointer, undoing the fix.
    echo "Lock them from the repository root (this stages the conversion):" >&2
    echo "  git -C \"\$(git rev-parse --show-toplevel)\" annex lock $RAW_DIR" >&2
    echo >&2
    echo "If this is intentional, commit with override:" >&2
    echo "  GA_ALLOW_RAW=1 git commit -m \"...\"" >&2
    exit 1
fi
