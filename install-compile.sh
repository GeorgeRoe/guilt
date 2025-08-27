#!/usr/bin/env sh
set -e

REPO="GeorgeRoe/guilt"
INSTALL_DIR="$HOME/.local/bin"
BIN_NAME="guilt"

# Ensure Rust is installed
if ! command -v cargo >/dev/null 2>&1; then
  echo "Rust (cargo) not found. Please install via https://rustup.rs/"
  exit 1
fi

# Clone and build
TMP_DIR=$(mktemp -d)
git clone "https://github.com/$REPO.git" "$TMP_DIR"
cd "$TMP_DIR"
cargo build --release

# Install binary
mkdir -p "$INSTALL_DIR"
cp "target/release/$BIN_NAME" "$INSTALL_DIR/"

echo "Installed to $INSTALL_DIR/$BIN_NAME"
echo "Make sure $INSTALL_DIR is in your PATH"