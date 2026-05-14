#!/usr/bin/env bash
# Regenerate patches/lerobot/local-fixes.patch from the current submodule
# working tree, and refresh BASE_COMMIT to the submodule's current HEAD.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PATCH_DIR="$ROOT/patches/lerobot"
SUBMODULE="$ROOT/lerobot"
PATCH="$PATCH_DIR/local-fixes.patch"
BASE_FILE="$PATCH_DIR/BASE_COMMIT"

mkdir -p "$PATCH_DIR"

# Use --no-color and stable timestamps so the file is reproducible.
git -C "$SUBMODULE" diff --no-color > "$PATCH"

if [[ ! -s "$PATCH" ]]; then
    echo "ℹ️  No changes in submodule — wrote empty patch."
else
    lines=$(wc -l < "$PATCH")
    echo "✅ Wrote $PATCH ($lines lines)"
fi

git -C "$SUBMODULE" rev-parse HEAD > "$BASE_FILE"
echo "✅ Updated $BASE_FILE → $(cat "$BASE_FILE")"
