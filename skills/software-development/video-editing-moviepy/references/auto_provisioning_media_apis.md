# Auto-Provisioning Base Models for Media APIs

When building headless media automation services (like FastAPI for n8n), relying on users to manually download and place base models (like Piper TTS `.onnx` files) causes deployment friction.

Instead, embed a standalone Python script to fetch the default models directly from official sources, and trigger it during the application's startup phase if the target directory is empty.

## 1. Setup Script (setup_models.py)

Create a dedicated script that bypasses strict SSL checks and mimics a standard user-agent (useful for restrictive corporate networks or headless VPS setups).

```python
import os
import urllib.request
import ssl

# Bypass SSL verification issues on some environments
ssl._create_default_https_context = ssl._create_unverified_context
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPER_DIR = os.path.join(BASE_DIR, "pretrained_models", "piper_voices")

DEFAULT_MODELS = {
    "en_US-lessac-medium": {
        "onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
        "json": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
    }
}

def setup_default_models():
    os.makedirs(PIPER_DIR, exist_ok=True)
    
    for model_name, urls in DEFAULT_MODELS.items():
        onnx_dest = os.path.join(PIPER_DIR, f"{model_name}.onnx")
        json_dest = os.path.join(PIPER_DIR, f"{model_name}.onnx.json")
        
        if os.path.exists(onnx_dest) and os.path.exists(json_dest):
            continue
            
        try:
            # Mask as a standard browser to prevent 403 Forbidden errors
            req_onnx = urllib.request.Request(urls["onnx"], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_onnx) as response, open(onnx_dest, 'wb') as out_file:
                out_file.write(response.read())
                
            req_json = urllib.request.Request(urls["json"], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_json) as response, open(json_dest, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Failed to download {model_name}: {e}")

if __name__ == "__main__":
    setup_default_models()
```

## 2. Bootstrapper Integration (app.py)

At the bottom of your main FastAPI entrypoint (before `app.run` or just standing alone for Uvicorn), check if the models exist. If they don't, spawn a subprocess to run the setup script.

```python
def ensure_base_models_exist():
    import os, subprocess
    piper_dir = os.path.join(BASE_DIR, "pretrained_models", "piper_voices")
    os.makedirs(piper_dir, exist_ok=True)
    
    # Check if there are any .onnx files
    if not any(f.endswith(".onnx") for f in os.listdir(piper_dir)):
        print("📥 [System] No Piper models found. Running Auto-Provisioning for Base Models...")
        try:
            subprocess.run(["python3", os.path.join(BASE_DIR, "setup_models.py")], check=True)
        except Exception as e:
            print(f"❌ [System] Auto-Provisioning failed: {e}")

ensure_base_models_exist()
```

## 3. Expose as an API Endpoint (For n8n)

Give workflow engines the ability to force a re-download or update without SSH access.

```python
@app.post("/api/models/download_defaults", tags=["Models"])
async def api_download_default_models():
    \"\"\"Endpoint for n8n to force download default Base Models\"\"\"
    try:
        import subprocess, os
        result = subprocess.run(["python3", os.path.join(BASE_DIR, "setup_models.py")], capture_output=True, text=True, check=True)
        return {"status": "success", "message": "Default models downloaded successfully", "details": result.stdout}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```