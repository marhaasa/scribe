#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if version argument is provided
if [ -z "$1" ]; then
  print_error "Please provide a version number (e.g., ./release.sh 0.2.0)"
  exit 1
fi

VERSION=$1

# Validate version format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  print_error "Version must be in format X.Y.Z (e.g., 0.2.0)"
  exit 1
fi

print_info "Preparing to release version $VERSION"

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
  print_error "You must be on the main branch to create a release"
  print_info "Current branch: $CURRENT_BRANCH"
  exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  print_error "You have uncommitted changes. Please commit or stash them first."
  exit 1
fi

# Pull latest changes
print_info "Pulling latest changes from origin..."
git pull origin main

# Update version in pyproject.toml
print_info "Updating version in pyproject.toml..."
poetry version $VERSION

# Update version in __init__.py
print_info "Updating version in scribe/__init__.py..."
echo "__version__ = \"$VERSION\"" >scribe/__init__.py

# Build the package to ensure it builds correctly
print_info "Testing build..."
poetry build

# Clean up test build
rm -rf dist/

# Commit version changes
print_info "Committing version changes..."
git add pyproject.toml scribe/__init__.py
git commit -m "Bump version to $VERSION"

# Push changes
print_info "Pushing changes to origin..."
git push origin main

# Create and push tag
print_info "Creating and pushing tag v$VERSION..."
git tag -a "v$VERSION" -m "Release version $VERSION"
git push origin "v$VERSION"

print_info "🎉 Release process completed!"
print_info "The GitHub Action will now:"
print_info "  1. Create a GitHub release"
print_info "  2. Build and upload Python packages"
print_info "  3. Update your homebrew tap automatically"
print_info ""
print_info "You can monitor the progress at:"
print_info "https://github.com/marhaasa/scribe/actions"
print_info ""
print_info "Once complete, users can install with:"
print_info "  brew tap marhaasa/tools"
print_info "  brew install scribe"
