# Infisical Installation Workarounds

When the official `.deb` script (via Cloudsmith) or GitHub release direct downloads fail (due to rate limits, geo-blocking, or broken repo configurations), do not fall into endless curl/wget retry loops. Use Docker to extract the pre-compiled binary directly from the official image.

```bash
# 1. Run a temporary container using the official CLI image
docker run -d --name temp_infisical infisical/cli sleep 30

# 2. Copy the binary from the container to the host
docker cp temp_infisical:/bin/infisical /tmp/infisical_bin

# 3. Clean up the container
docker rm -f temp_infisical

# 4. Move and make executable on the host
sudo mv /tmp/infisical_bin /usr/local/bin/infisical
sudo chmod +x /usr/local/bin/infisical

# 5. Verify
infisical --version
```