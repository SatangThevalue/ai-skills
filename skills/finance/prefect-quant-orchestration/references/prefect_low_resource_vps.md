# Handling Prefect / SQLite Concurrency on Low-Resource VPS

When running heavy ML pipelines (e.g., training 30 LightGBM models concurrently) on a low-resource VPS using Prefect and a local SQLite database, the system will likely fail with `database is locked` or CPU timeouts.

## Solutions
1. **Disable Prefect Daemon**: Set environment variables to run in pure offline mode.
   ```python
   os.environ["PREFECT_API_URL"] = ""
   os.environ["PREFECT_LOCAL_STORAGE_PATH"] = os.path.join(os.getcwd(), ".prefect")
   ```
2. **Sequential Queue**: Use `ThreadPoolTaskRunner(max_workers=1)` to force Prefect to process tasks sequentially, preventing SQLite concurrent write locks.
3. **Rate Limiting**: Apply `@task` rate limits when fetching data from external APIs (like Yahoo Finance) to prevent IP bans or timeouts.
4. **Fallback to Native Python**: If Prefect overhead is still too high for the VPS RAM, bypass Prefect entirely and run the pipeline via a native Python script using `nohup python script.py > log.txt 2>&1 &` to ensure completion as a background process.