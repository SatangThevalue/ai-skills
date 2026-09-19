# Rsync Exclude Patterns for Hermes Skills

When synchronizing local Hermes skills (`~/.hermes/skills/`) to a Git repository, always exclude the following internal state directories and files to prevent polluting the repository with environment-specific or transient data:

```bash
rsync -av \
  --exclude='.git' \
  --exclude='.curator_backups' \
  --exclude='.curator_state' \
  --exclude='.bundled_manifest' \
  ~/.hermes/skills/ ~/path-to-repo/skills/
```

- `.curator_backups` / `.curator_state`: Internal state for the background curator.
- `.bundled_manifest`: Manifest of bundled tools, not part of user skill data.