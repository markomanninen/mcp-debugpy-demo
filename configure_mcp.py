#!/usr/bin/env python3
"""
Configure MCP settings for the mcp-debugpy-demo project.
Automatically detects the OS and generates the correct configuration files.
"""

import json
import os
import platform
import sys
from pathlib import Path


def get_project_root():
    """Get the absolute path to the project root directory."""
    return Path(__file__).parent.resolve()


def get_mcp_server_path():
    """Get the OS-specific path to the mcp-debug-server executable."""
    project_root = get_project_root()
    system = platform.system()

    if system == "Windows":
        # Windows uses Scripts directory and .exe extension
        return project_root / ".venv" / "Scripts" / "mcp-debug-server.exe"
    else:
        # Unix-like systems (Linux, macOS) use bin directory
        return project_root / ".venv" / "bin" / "mcp-debug-server"


def create_mcp_json():
    """Create .mcp.json for Claude CLI with absolute paths."""
    project_root = get_project_root()
    mcp_server_path = get_mcp_server_path()

    config = {
        "mcpServers": {
            "agentDebug": {
                "type": "stdio",
                "command": str(mcp_server_path),
                "args": [],
                "env": {}
            }
        }
    }

    config_path = project_root / ".mcp.json"

    # Write with proper formatting
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[OK] Created {config_path}")
    return config_path


def create_vscode_mcp_json():
    """Create .vscode/mcp.json for VS Code with workspace-relative paths."""
    project_root = get_project_root()
    vscode_dir = project_root / ".vscode"
    vscode_dir.mkdir(exist_ok=True)

    system = platform.system()

    # Use Path to construct the relative path - OS-appropriate separators
    if system == "Windows":
        rel_path = Path(".venv") / "Scripts" / "mcp-debug-server.exe"
    else:
        rel_path = Path(".venv") / "bin" / "mcp-debug-server"

    # VS Code uses forward slashes on all platforms, so use as_posix()
    command = "${workspaceFolder}/" + rel_path.as_posix()

    config = {
        "servers": {
            "agentDebug": {
                "type": "stdio",
                "command": command,
                "args": [],
                "cwd": "${workspaceFolder}"
            }
        },
        "inputs": []
    }

    config_path = vscode_dir / "mcp.json"

    # Write with proper formatting
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[OK] Created {config_path}")
    return config_path


def verify_mcp_server_exists():
    """Verify that the mcp-debug-server executable exists."""
    mcp_server_path = get_mcp_server_path()

    if not mcp_server_path.exists():
        print(f"[WARN] MCP server not found at: {mcp_server_path}")
        print("[WARN] Make sure you've run the setup script and installed mcp-debugpy")
        return False

    print(f"[OK] MCP server found at: {mcp_server_path}")
    return True


def main():
    """Main configuration function."""
    print("=" * 60)
    print("Configuring MCP settings for mcp-debugpy-demo")
    print("=" * 60)
    print()

    # Detect OS
    system = platform.system()
    print(f"Detected OS: {system}")
    print(f"Project root: {get_project_root()}")
    print()

    # Verify MCP server exists
    server_exists = verify_mcp_server_exists()
    print()

    # Create configuration files
    try:
        mcp_json_path = create_mcp_json()
        vscode_mcp_json_path = create_vscode_mcp_json()
        print()

        print("=" * 60)
        print("Configuration complete!")
        print("=" * 60)
        print()

        if not server_exists:
            print("[WARN] MCP server executable not found.")
            print("Please ensure you've completed the setup:")
            if system == "Windows":
                print("  1. Run: setup.bat")
            else:
                print("  1. Run: ./setup.sh")
            print("  2. Verify mcp-debugpy is installed")
            print()

        print("Configuration files created:")
        print(f"  - {mcp_json_path} (for Claude CLI)")
        print(f"  - {vscode_mcp_json_path} (for VS Code)")
        print()

        print("Next steps:")
        print("  1. Restart Claude CLI or VS Code to pick up the new configuration")
        print("  2. In Claude CLI, the 'agentDebug' server should now be available")
        print("  3. Try debugging: 'Debug shopping_cart.py using breakpoints'")
        print()

    except Exception as e:
        print(f"[ERROR] Failed to create configuration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
