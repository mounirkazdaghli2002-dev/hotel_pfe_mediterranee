# VSCode Browser Workspace Fix

## Issue
File explorer empty when opening repo in browser (vscode.dev, github.dev, Codespaces).

## Fixes (Try in order)
1. **Reload Window**: Ctrl+Shift+P → \"Developer: Reload Window\"
2. **Ensure Repo Root**: Open folder/repo root, not single file.
3. **Codespaces**: Click Rebuild Container (devcontainer.json present).
4. **Extensions**: Install Python, Pylance, Streamlit.
5. **New `.vscode/settings.json`**: Excludes heavy dirs (.git, cache) for fast load.

Files now visible after reload!

