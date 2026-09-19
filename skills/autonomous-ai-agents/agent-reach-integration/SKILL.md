---
name: agent-reach-integration
description: "Install, configure, and operate the Agent Reach (Panniantong) framework to give agents internet channel access (X, Reddit, Bilibili, YouTube, Exa)."
tags: [agent-reach, internet, scraping, mcp, social-media]
---
# Agent Reach Integration

Agent Reach (by Panniantong) is a tool manager that installs and configures external channels (CLI/MCP) to give AI agents access to platforms like Twitter, Reddit, YouTube, GitHub, Bilibili, and Exa Search.

## ⚠️ Critical Pitfalls

1. **PyPI Name Collision:** Do NOT `pip install agent-reach`. The package on PyPI belongs to a different project by a different author. Always install directly from the GitHub archive:
   `https://github.com/Panniantong/agent-reach/archive/main.zip`
2. **PEP 668 (Externally Managed):** If the system Python is externally managed, use `pipx` or create a dedicated virtual environment (e.g., `python3 -m venv ~/.agent-reach-venv`) to avoid installation failures.
3. **Node.js Version for mcporter:** The `mcporter` tool (used for Exa semantic search and LinkedIn) requires **Node.js >= 24**. Older versions (e.g., v12) will fail with `EBADENGINE`. Ensure Node is updated before attempting to install `mcporter`.
4. **Dotfile Overwrite Blocks:** Commands that redirect output to dotfiles (e.g., `echo "..." >> ~/.bashrc` or `echo "..." >> ~/.config/yt-dlp/config`) may trigger security scanner blocks (e.g., `tirith:dotfile_overwrite`).
   * *Workaround 1:* Symlink binaries to `~/.local/bin/` instead of modifying `~/.bashrc`.
   * *Workaround 2:* Provide the exact commands to the user to run manually if system changes require explicit approval.

## Installation Workflow

```bash
# 1. Create venv and install
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install https://github.com/Panniantong/agent-reach/archive/main.zip

# 2. Expose binary safely (avoiding .bashrc overwrite if blocked)
mkdir -p ~/.local/bin
ln -s ~/.agent-reach-venv/bin/agent-reach ~/.local/bin/agent-reach

# 3. Safe diagnostic check
~/.local/bin/agent-reach install --env=auto --safe
~/.local/bin/agent-reach doctor
```

## Channel Configuration

- **Zero-config channels:** Jina Reader, RSS, GitHub (if `gh` authenticated), V2EX, Bilibili (basic search).
- **Requires Node/NPM:** Exa Search (requires `npm install -g mcporter`), YouTube `yt-dlp` (requires node runtime config `grep -qxF -- '--js-runtimes node' ~/.config/yt-dlp/config`).
- **Requires User Cookies:** Twitter, Reddit, XiaoHongShu, Xueqiu, Facebook, Instagram. Run `agent-reach configure <channel>` and ask the user to export Header Strings using the Cookie-Editor Chrome extension.
- **Requires Proxy:** Set `HTTP_PROXY` and `HTTPS_PROXY` for channels like Reddit or Twitter if the server IP is restricted/blocked.

## Usage Guidelines

Agent Reach is an installer/router, not a wrapper. Once installed, invoke the upstream tools directly in the shell:

- **Web:** `curl -s "https://r.jina.ai/URL"`
- **YouTube:** `yt-dlp --dump-json URL`
- **Twitter:** `export TWITTER_AUTH_TOKEN=*** export TWITTER_CT0="..."; twitter search "query" -n 10`
- **Bilibili:** `bili search "query" --type video`
- **GitHub:** `gh search repos "query"`
- **Exa Search:** `mcporter call exa.web_search_exa query="..." numResults=5`
