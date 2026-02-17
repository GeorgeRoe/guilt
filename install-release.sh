#!/usr/bin/env sh
set -e

REPO="SCD-Energy-Efficiency-Team/guilt"
INSTALL_DIR="$HOME/.local/bin"
BIN_NAME="guilt"

mkdir -p "$INSTALL_DIR"

# Detect architecture
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64)
    ASSET_NAME="guilt-x86_64"
    ;;
  aarch64 | arm64)
    ASSET_NAME="guilt-aarch64"
    ;;
  *)
    echo "Error: Unsupported architecture: $ARCH"
    exit 1
    ;;
esac

# Get latest release URL for the correct asset
LATEST_URL=$(curl -s https://api.github.com/repos/$REPO/releases/latest \
  | jq -r ".assets[] | select(.name==\"$ASSET_NAME\") | .browser_download_url")

if [ -z "$LATEST_URL" ]; then
  echo "Error: Could not find latest release URL for $BIN_NAME on $ARCH"
  exit 1
fi

curl -L "$LATEST_URL" -o "$INSTALL_DIR/$BIN_NAME"
chmod +x "$INSTALL_DIR/$BIN_NAME"

echo "$BIN_NAME installed to $INSTALL_DIR"
echo "Make sure $INSTALL_DIR is in your PATH"