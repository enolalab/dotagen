#!/bin/sh
# dotagen install script — downloads the latest release binary
# Usage: curl -fsSL https://raw.githubusercontent.com/enolalabs/dotagen/main/install.sh | sh
# Or:    wget -qO- https://raw.githubusercontent.com/enolalabs/dotagen/main/install.sh | sh

set -e

REPO="enolalabs/dotagen"
BINARY_NAME="dotagen"

# ── Detect OS ──
OS=$(uname -s)
case "$OS" in
    Linux*)  PLATFORM="linux";;
    Darwin*) PLATFORM="darwin";;
    MINGW*|MSYS*|CYGWIN*) PLATFORM="windows";;
    *) echo "Unsupported OS: $OS"; exit 1;;
esac

# ── Detect Architecture ──
ARCH=$(uname -m)
case "$ARCH" in
    x86_64|amd64)  ARCH="amd64";;
    aarch64|arm64) ARCH="arm64";;
    i386|i686)     ARCH="386";;
    *) echo "Unsupported architecture: $ARCH"; exit 1;;
esac

# ── Get latest release version ──
printf "Fetching latest release... "
if command -v curl >/dev/null 2>&1; then
    VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name"' | head -1 | sed -E 's/.*"([^"]+)".*/\1/')
else
    VERSION=$(wget -qO- "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name"' | head -1 | sed -E 's/.*"([^"]+)".*/\1/')
fi

if [ -z "$VERSION" ]; then
    echo "FAILED"
    echo "Could not determine latest version. Check your internet connection."
    exit 1
fi
printf "%s\n" "$VERSION"

# ── Build download URL ──
if [ "$PLATFORM" = "windows" ]; then
    ASSET="${BINARY_NAME}_${VERSION#v}_${PLATFORM}_${ARCH}.exe"
    BINARY_NAME="dotagen.exe"
else
    ASSET="${BINARY_NAME}_${VERSION#v}_${PLATFORM}_${ARCH}"
fi
URL="https://github.com/${REPO}/releases/download/${VERSION}/${ASSET}"

# ── Download ──
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

printf "Downloading %s/%s... " "$PLATFORM" "$ARCH"
if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "$TMPDIR/$BINARY_NAME" "$URL"
else
    wget -q -O "$TMPDIR/$BINARY_NAME" "$URL"
fi

if [ ! -s "$TMPDIR/$BINARY_NAME" ]; then
    echo "FAILED"
    echo "Binary not found for ${PLATFORM}/${ARCH}. URL: $URL"
    exit 1
fi
chmod +x "$TMPDIR/$BINARY_NAME"
printf "OK\n"

# ── Install ──
INSTALL_DIR=""
INSTALL_PATHS="/usr/local/bin:$HOME/.local/bin:$HOME/bin"

for dir in $(echo "$INSTALL_PATHS" | tr ':' ' '); do
    if [ -d "$dir" ] && [ -w "$dir" ]; then
        INSTALL_DIR="$dir"
        break
    fi
done

if [ -z "$INSTALL_DIR" ]; then
    for dir in /usr/local/bin "$HOME/.local/bin" "$HOME/bin"; do
        mkdir -p "$dir" 2>/dev/null && INSTALL_DIR="$dir" && break
    done
fi

if [ -z "$INSTALL_DIR" ]; then
    echo "Could not find a writable install directory."
    echo "Manual install: cp $TMPDIR/$BINARY_NAME /your/bin/"
    exit 1
fi

mv "$TMPDIR/$BINARY_NAME" "$INSTALL_DIR/$BINARY_NAME"
printf "Installed to %s/%s\n" "$INSTALL_DIR" "$BINARY_NAME"

# ── Verify ──
case "$PATH" in
    *"$INSTALL_DIR"*) ;;
    *)
        printf "\n%s is not in your PATH. Add it:\n" "$INSTALL_DIR"
        if [ -f "$HOME/.zshrc" ]; then
            printf '  echo '\''export PATH="%s:$PATH"'\'' >> ~/.zshrc\n' "$INSTALL_DIR"
        else
            printf '  echo '\''export PATH="%s:$PATH"'\'' >> ~/.bashrc\n' "$INSTALL_DIR"
        fi
        printf '  source ~/.zshrc  # or ~/.bashrc\n\n'
        ;;
esac

printf "\ndotagen installed successfully!\n"
printf "Run: dotagen init\n"
