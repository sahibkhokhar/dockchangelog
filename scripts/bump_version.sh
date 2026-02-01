#!/bin/bash
# Helper script to bump version and prepare for release

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: ./scripts/bump_version.sh <new_version>"
    echo "Example: ./scripts/bump_version.sh 0.5.1"
    exit 1
fi

NEW_VERSION=$1
OLD_VERSION=$(grep -oP '__version__ = "\K[^"]+' src/dockchangelog/__init__.py)

echo "Bumping version: $OLD_VERSION → $NEW_VERSION"

# Update __init__.py
sed -i "s/__version__ = \"$OLD_VERSION\"/__version__ = \"$NEW_VERSION\"/" src/dockchangelog/__init__.py

# Update pyproject.toml
sed -i "s/^version = \"$OLD_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml

echo "✓ Updated src/dockchangelog/__init__.py"
echo "✓ Updated pyproject.toml"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit: git add . && git commit -m 'Bump version to $NEW_VERSION'"
echo "  3. Tag: git tag v$NEW_VERSION"
echo "  4. Push: git push origin main --tags"
echo "  5. Create GitHub Release at: https://github.com/sahibkhokhar/dockchangelog/releases/new"
