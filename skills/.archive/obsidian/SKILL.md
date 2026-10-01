---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault. Provides vault-first templates, canonical data schema, and repeatable scripts for financial-ledger workflows in Obsidian.
platforms: [linux, macos, windows]
---
metadata:
  hermes:
    reviewed: "2026-06-01 (automated)"

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

This skill now includes:
- Quickstart install options for Linux (AppImage / .deb / Snap) and a safe AppImage launcher pattern.
- Recommended vault layout and starter templates for financial ledgers (transactions.csv, accounts.yml, daily note template).
- Canonical numeric storage guidance (amount_in_cents / Decimal, ISO-8601 dates).
- Small verification scripts (validate_transactions.py) and template files under `templates/` and `scripts/`.
- Pitfalls & troubleshooting notes for common environment issues (sudo in noninteractive shells, AppImage permissions, desktop entry creation).

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `~/.hermes/.env`. If it is unset, use `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

## Quickstart (Linux) - AppImage recommended when sudo not available

- Preferred for automation and hermes-managed environments: AppImage.
- Typical steps (what Hermes does when asked):
  1. Download latest AppImage to ~/Applications/Obsidian.AppImage
  2. chmod +x the AppImage
  3. Create a tiny launcher at ~/.local/bin/obsidian that runs the AppImage
  4. Create a desktop file in ~/.local/share/applications/obsidian.desktop with Exec pointing to the AppImage

Notes:
- Installing the .deb package via dpkg requires sudo and an interactive password prompt. In noninteractive or remote sessions prefer AppImage unless the user explicitly provides sudo access.
- AppImage keeps Obsidian self-contained and is easy to update by replacing the file.

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Templates & recommended vault layout (financial ledger)

When building a finance-focused vault, prefer a mixed approach:
- Human-readable notes: Markdown files with YAML frontmatter for metadata. Use Obsidian templates for daily notes, policy, and narratives.
- Source-of-truth (SoT): a canonical CSV or SQLite ledger for numeric data and computations. Store amounts as integer minor-units (amount_cents) or as strings parsed with Decimal to avoid floating point errors.

Recommended minimal layout (create under vault root):
- Templates/
  - Daily Template.md
  - transaction-template.md
- transactions.csv (canonical ledger, one file or NDJSON)
- accounts.yml
- scripts/validate_transactions.py
- references/transactions-schema.md

This skill ships example support files in its `templates/`, `scripts/`, and `references/` directories that agents can write into a user's vault on request.

## Appendix: Canonical ledger schema (guidance)

- transactions.csv headers (recommended):
  id,date,account,counterparty,category,amount_cents,currency,type,tags,notes,source_file,created_at

- Numeric rules:
  - Store money as integer minor units (e.g., 12345 for 123.45 THB) in `amount_cents` or store as exact decimal string and parse with Decimal on read.
  - Use ISO-8601 for dates: YYYY-MM-DD or full timestamps when needed.

## Append & Targeted edits

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Tools & plugins (Obsidian)

Recommended plugins for vault workflows:
- Dataview — query and aggregate numbers in your notes
- Templater — create and insert templates (daily notes, transaction templates)
- Advanced Tables / CSV preview — view and edit CSVs in-vault

## Automation & common scripts

This skill recognizes that many finance tasks benefit from small Python helper scripts:
- validate_transactions.py — validate header, integer amounts, and basic totals
- importers — map bank CSV to canonical transactions.csv (user-specific mapping)

The skill includes example scripts under `scripts/` that agents can copy to the user's vault and run.

## Pitfalls & troubleshooting

- Running dpkg/apt with sudo inside a Hermes terminal may fail without a TTY; prefer AppImage if user does not grant interactive sudo.
- When creating desktop files or launchers, ensure AppImage is executable (chmod +x) and the Exec path is absolute.
- Obsidian's GUI must be launched in a graphical session; AppImage will not start in purely headless CI unless X/Wayland is available.
- Use Git for vault backup. If user wants automatic backups, set up a small cron or GitHub Action to commit/export periodically.

## Where this skill writes support files

Use skill_manage write_file to add support files under:
- references/transactions-schema.md — short schema + rationales
- templates/Daily Template.md — daily note template
- templates/transactions.csv — starter CSV header
- scripts/validate_transactions.py — validator script


## Examples (commands agent can run)
- Download AppImage and prepare launcher (AppImage path, launcher):
  - Place AppImage at ~/Applications/Obsidian.AppImage, chmod +x, write launcher at ~/.local/bin/obsidian, create desktop file at ~/.local/share/applications/obsidian.desktop
- Validate ledger:
  - python3 "{vault}/scripts/validate_transactions.py"


## References
See the `references/`, `templates/`, and `scripts/` files packaged with this skill for session-proven examples and re-runnable scripts.
