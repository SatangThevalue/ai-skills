# Fix: ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY in Docker

When running `pnpm install` inside a Dockerfile build step, it may fail with:
`ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY Aborted removal of modules directory due to no TTY`

**Cause:**
pnpm sometimes attempts to clean up existing `node_modules`. Without a TTY (like in a CI or Docker build environment), it pauses for a confirmation prompt (Y/n), fails to get input, and aborts the build.

**Solution:**
Force pnpm into CI mode and explicitly disable the purge confirmation prompt before running install. 

In your Dockerfile:
```dockerfile
# Force pnpm to install in CI mode (bypass TTY prompt)
ENV CI=true

# Explicitly disable the purge confirmation
RUN pnpm config set confirmModulesPurge false

# Install dependencies (add --frozen-lockfile=false if your lockfile is out of sync)
RUN pnpm install
```