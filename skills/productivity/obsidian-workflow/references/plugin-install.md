Plugin manual-install notes

When to use: offline installs or reproducible CI builds where the community plugin marketplace is unavailable.

Pattern:
1. Identify plugin GitHub repo and open Releases page.
2. Download required assets for the latest release: manifest.json, main.js (or index.js), styles.css (if present).
3. Create target folder: .obsidian/plugins/<plugin-id>/
4. Place assets inside that folder. Ensure manifest.json and main.js exist.
5. In Vault: .obsidian/community-plugins.json, add plugin id to enabled list (restart Obsidian if necessary).

Notes & gotchas:
- Some plugins bundle assets under dist/; the release may include the files under different names. Check release assets list to pick correct files.
- Verify plugin manifest version matches Obsidian API/engine version if plugin fails to load.
- Templater requires user config: template folder path and enable "templater user scripts" (done in UI).
- Dataview is purely a JS plugin; installing main.js + manifest.json + styles.css is usually sufficient.
