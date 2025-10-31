#!/bin/bash
# Setup script for mcp-debugpy-demo

set -e

echo "Setting up mcp-debugpy-demo..."

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Found Python version: $PYTHON_VERSION"

# Create virtual environment
echo "Creating virtual environment..."
python -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install pytest pytest-asyncio

# Install mcp-debugpy from source
echo "Installing mcp-debugpy from GitHub..."
pip install git+https://github.com/markomanninen/mcp-debugpy.git

echo ""
echo "Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the buggy application:"
echo "  python shopping_cart.py"
echo ""
echo "To run tests and see the bug:"
echo "  pytest test_shopping_cart.py -v"
echo ""
echo "To configure MCP for VS Code, the settings are already in .vscode/settings.json"
echo "Make sure you have the MCP extension installed in VS Code."
echo ""
