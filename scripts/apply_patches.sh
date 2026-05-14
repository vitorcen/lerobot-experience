#!/usr/bin/env bash
# Apply local patches to the lerobot submodule. Idempotent: skips a patch that
# is already applied (detected via `git apply --reverse --check`).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PATCH_DIR="$ROOT/patches/lerobot"
SUBMODULE="$ROOT/lerobot"
PATCH="$PATCH_DIR/local-fixes.patch"
BASE_FILE="$PATCH_DIR/BASE_COMMIT"

if [[ ! -d "$SUBMODULE/.git" && ! -f "$SUBMODULE/.git" ]]; then
    echo "❌ Submodule '$SUBMODULE' is not initialized. Run: git submodule update --init"
    exit 1
fi

if [[ ! -f "$PATCH" ]]; then
    echo "ℹ️  No patch found at $PATCH — nothing to apply."
    exit 0
fi

# Warn if submodule HEAD has drifted from the commit the patch was made against.
if [[ -f "$BASE_FILE" ]]; then
    expected=$(tr -d '[:space:]' < "$BASE_FILE")
    actual=$(git -C "$SUBMODULE" rev-parse HEAD)
    if [[ "$expected" != "$actual" ]]; then
        echo "⚠️  Submodule HEAD ($actual) differs from BASE_COMMIT ($expected)."
        echo "   The patch may not apply cleanly. Continuing anyway."
    fi
fi

cd "$SUBMODULE"

# Already applied? `git apply --reverse --check` succeeds iff the diff cleanly
# reverses, i.e. the changes are present.
if git apply --reverse --check "$PATCH" >/dev/null 2>&1; then
    echo "✅ Patches already applied — nothing to do."
    exit 0
fi

if ! git apply --check "$PATCH" >/dev/null 2>&1; then
    echo "❌ Patch does not apply cleanly to $SUBMODULE."
    echo "   Diagnostic output:"
    git apply --check "$PATCH" || true
    exit 1
fi

git apply "$PATCH"
echo "✅ Applied patches/lerobot/local-fixes.patch"
