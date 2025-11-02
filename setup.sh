#!/usr/bin/env bash
# Setup script for mcp-debugpy-demo

set -euo pipefail

echo "Setting up mcp-debugpy-demo..."

# Find a suitable Python executable. Prefer python, then python3, then any
# python3.X available on PATH.
PY_CANDIDATES=(python python3 python3.13 python3.12 python3.11 python3.10 python3.9 python3.8)
PYTHON=""
for p in "${PY_CANDIDATES[@]}"; do
	if command -v "$p" >/dev/null 2>&1; then
		# check version
		ver=$($p --version 2>&1 | awk '{print $2}') || true
		# parse major and minor
		major=$(echo "$ver" | cut -d. -f1 || echo 0)
		minor=$(echo "$ver" | cut -d. -f2 || echo 0)
		if [[ "$major" -ge 3 && "$minor" -ge 8 ]] || ([[ "$major" -ge 4 ]]); then
			PYTHON="$p"
			PYTHON_VERSION="$ver"
			break
		fi
	fi
done

if [[ -z "${PYTHON}" ]]; then
	echo "ERROR: Could not find a Python >= 3.8 on PATH. Please install Python 3.8+ or create a virtualenv yourself."
	exit 1
fi

echo "Found Python executable: ${PYTHON} (version ${PYTHON_VERSION})"

# Create virtual environment unless it already exists
if [[ -d ".venv" ]]; then
	echo ".venv already exists — reusing existing virtual environment."
else
	echo "Creating virtual environment with ${PYTHON}..."
	"${PYTHON}" -m venv .venv
fi

echo "Activating virtual environment..."
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Upgrading pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel || true

if [[ -f "requirements.txt" ]]; then
	echo "Installing dependencies from requirements.txt..."
	pip install -r requirements.txt || {
		echo "Failed to install requirements from requirements.txt — continuing but you may need to install them manually." >&2
	}
else
	echo "No requirements.txt found; installing minimal test deps..."
	pip install pytest pytest-asyncio || true
fi

echo "Attempting to install mcp-debugpy from GitHub (optional)..."
if pip install --no-deps --upgrade git+https://github.com/markomanninen/mcp-debugpy.git; then
	echo "Installed mcp-debugpy from GitHub."
else
	echo "Could not install mcp-debugpy from GitHub. This is optional for the demo; you can install it later with:"
	echo "  .venv/bin/pip install git+https://github.com/markomanninen/mcp-debugpy.git"
fi

echo ""
echo "Configuring MCP settings for this system..."
if python configure_mcp.py; then
	echo "MCP configuration created successfully."
else
	echo "WARNING: Failed to configure MCP settings. You may need to configure manually."
fi

echo ""
echo "Setup complete!"
echo ""
echo "To activate the environment, run:" 
echo "  source .venv/bin/activate"
echo "or use the venv Python directly:" 
echo "  .venv/bin/python shopping_cart.py"
echo ""
echo "To run the buggy application (without activating):"
echo "  .venv/bin/python shopping_cart.py"
echo ""
echo "To run tests (without activating):"
echo "  .venv/bin/pytest test_shopping_cart.py -v"
echo ""
echo "To configure MCP for VS Code, the settings are already in .vscode/settings.json"
echo "Make sure you have the MCP extension installed in VS Code."
echo ""
