#!/usr/bin/env sh
set -e

REPO="GeorgeRoe/guilt"
BIN_NAME="guilt"
INSTALL_DIR="$HOME/.local/bin"

mkdir -p "$INSTALL_DIR"

LATEST_URL=$(curl -s https://api.github.com/repos/$REPO/releases/latest \
  | jq -r '.assets[] | select(.name | contains("guilt")) | .browser_download_url')


if [ -z "$LATEST_URL" ]; then
  echo "Error: Could not find latest release URL for $BIN_NAME"
  exit 1
fi

curl -L "$LATEST_URL" -o "$INSTALL_DIR/$BIN_NAME"
chmod +x "$INSTALL_DIR/$BIN_NAME"

echo "$BIN_NAME installed to $INSTALL_DIR"
echo "Make sure $INSTALL_DIR is in your PATH"