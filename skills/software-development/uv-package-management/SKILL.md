---
name: uv-package-management
description: Manage Python dependencies and virtual environments using uv.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Python
      - UV
      - Package-Manager
      - Dependencies
---

# Python Package Management with UV

`uv` is an extremely fast Python package installer and resolver designed as a drop-in replacement for `pip`, `pip-tools`, and `virtualenv`.

## When to Use
- When installing Python packages on a VPS or target machine.
- When creating, managing, or activating virtual environments (`.venv`).
- When locking dependencies using `uv pip compile`.

## Prerequisites
- `uv` binary installed on the system (already installed on this machine).
- A Python interpreter available on the system path.

## How to Run
- Run all `uv` setup and installation commands through the `terminal` tool.

## Quick Reference
- Create virtual env: `uv venv`
- Install packages: `uv pip install <package>`
- Compile lockfile: `uv pip compile requirements.in -o requirements.txt`
- Sync environment: `uv pip sync requirements.txt`

## Procedure

1. **Create a Virtual Environment**
   Initialize a new virtual environment in the project directory:
   ```bash
   uv venv
   ```

2. **Activate the Environment**
   ```bash
   source .venv/bin/activate
   ```

3. **Install Packages**
   Install packages directly using uv:
   ```bash
   uv pip install fastapi uvicorn
   ```

4. **Lock and Sync Dependencies**
   Create a `requirements.in` file listing top-level dependencies, then compile and sync:
   ```bash
   uv pip compile requirements.in -o requirements.txt
   uv pip sync requirements.txt
   ```

## Pitfalls
- **Global Installations**: Avoid running `uv pip install` outside a virtual environment unless explicitly using the `--system` flag.
- **Python Version Mismatches**: Use `uv venv --python 3.11` to specify a specific Python version if multiple versions are installed.

## Verification
Verify the installation of packages inside the virtual environment:
```bash
uv pip list
```
