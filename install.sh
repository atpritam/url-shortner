#!/bin/bash

# Ulauncher URL Shortener Extension - Installation Script

set -e

EXTENSION_NAME="ulauncher-url-shortener"
EXTENSIONS_DIR="$HOME/.local/share/ulauncher/extensions"
INSTALL_DIR="$EXTENSIONS_DIR/$EXTENSION_NAME"

echo "========================================="
echo "URL Shortener Extension Installer"
echo "========================================="
echo ""

if ! command -v ulauncher &> /dev/null; then
    echo "  Warning: Ulauncher doesn't appear to be installed."
    echo "   Please install Ulauncher first: https://ulauncher.io/"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo " Creating extensions directory..."
mkdir -p "$EXTENSIONS_DIR"

if [ -d "$INSTALL_DIR" ]; then
    echo "  Extension already exists at: $INSTALL_DIR"
    read -p "Remove existing installation? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
        echo "✓ Removed existing installation"
    else
        echo "Installation cancelled."
        exit 1
    fi
fi

echo " Installing extension files..."
mkdir -p "$INSTALL_DIR"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/" 2>/dev/null || true

echo " Installing Python dependencies..."
echo ""

INSTALL_SUCCESS=false

echo "Checking if dependencies are already installed..."
if python3 -c "import requests, pyperclip" 2>/dev/null; then
    INSTALL_SUCCESS=true
    echo "✓ Dependencies already installed!"
fi

if [ "$INSTALL_SUCCESS" = false ]; then
    echo "Attempting installation with pip..."
    if command -v pip3 &> /dev/null; then
        if pip3 install --user --break-system-packages requests pyperclip 2>/dev/null; then
            INSTALL_SUCCESS=true
            echo "✓ Installed with pip3"
        fi
    elif command -v pip &> /dev/null; then
        if pip install --user --break-system-packages requests pyperclip 2>/dev/null; then
            INSTALL_SUCCESS=true
            echo "✓ Installed with pip"
        fi
    fi
fi

if [ "$INSTALL_SUCCESS" = false ]; then
    echo ""
    echo "  Could not install Python dependencies automatically."
    echo ""
    echo "Please install manually using ONE of these methods:"
    echo ""
    echo "Option 1 (Recommended): Use your system package manager"
    echo "  sudo apt install python3-requests python3-pyperclip  # Debian/Ubuntu"
    echo "  sudo dnf install python3-requests python3-pyperclip  # Fedora"
    echo "  sudo pacman -S python-requests python-pyperclip      # Arch"
    echo ""
    echo "Option 2: Use pip with --break-system-packages"
    echo "  pip3 install --user --break-system-packages requests pyperclip"
    echo ""
    read -p "Press Enter to continue anyway..."
fi

echo ""
echo "========================================="
echo " Installation complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Restart Ulauncher or press Ctrl+Alt+R to reload"
echo "2. Open Ulauncher (usually Ctrl+Space)"
echo "3. Type 'short' followed by a URL to shorten"
echo ""
echo "To configure the extension:"
echo "- Open Ulauncher Preferences → Extensions"
echo "- Find 'URL Shortener' and customize settings"
echo ""