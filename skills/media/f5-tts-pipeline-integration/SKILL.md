---
name: f5-tts-pipeline-integration
description: Train and serve voice cloning models on Colab and VPS.
version: 0.1.0
metadata:
  hermes:
    tags:
      - TTS
      - F5-TTS
      - Voice-Cloning
      - Machine-Learning
---

# F5-TTS Dual-Environment Pipeline Integration

Integrates F5-TTS Flow Matching voice cloning across low-spec VPS hosts and GPU-accelerated Google Colab environments. Handles model adapters, in-context reference chunk selection, studio DSP mastering, and dual-mode testing. Does not support non-commercial model weights; all pipelines strictly use MIT-licensed weights and libraries.

## When to Use

- "integrate F5-TTS into TTS pipeline"
- "fix Colab training mock stub to real F5-TTS"
- "add pre-export sound check for TTS checkpoints"
- "verify TTS master pipeline across VPS and Colab"
- "deploy F5-TTS voice cloning with studio mastering"

## Prerequisites

- Python 3.10+ with `uv` package manager installed.
- Repositories: `SatangThevalue/satangthevalue-tts-custom`.
- GPU Environment (Google Colab / RunPod):
  - Dependencies: `pip install f5-tts vocos pedalboard soundfile`
  - Weights: `SWivid/F5-TTS` (MIT License) downloaded or cached in Google Drive.
- Low-spec Environment (VPS):
  - Requires headless test compatibility without PyTorch/CUDA via fallback simulation.

## How to Run

1. Inspect existing models and adapters using `search_files` and `read_file`.
2. Implement or update inference and adapters using `patch` or `write_file`.
3. Run the full verification test suite using the `terminal` tool.
4. Synchronize notebooks and push verified code using git in `terminal`.

## Quick Reference

| Command / Component | Location / Signature |
|---|---|
| Master Test Suite | `python3 tests/test_master_pipeline.py` |
| Real F5 Inference | `from src.inference.f5_infer import synthesize_f5` |
| Checkpoint Preview | `from src.inference.test_checkpoint import preview_checkpoint` |
| Engine Entrypoint | `from src.inference.engine import VoiceInferenceEngine, TTSEngine` |
| Voice Quality Evaluator | `from src.evaluation.voice_evaluator import evaluate_synthesized_voice` |
| Diagnostics Reference | `references/finetune_diagnostics.md` |
| Colab Pipeline | `notebooks/colab_pipeline.ipynb` |

## Procedure

1. **Verify Interface Contract Before Implementation**
   Use `read_file` to inspect `src/models/base_adapter.py`. Ensure any new or modified adapter implements all four abstract methods:
   - `load_base_weights(weights_path: str)`
   - `build_lora_model(lora_config: Dict[str, Any])`
   - `export_onnx(checkpoint_path: str, output_onnx_path: str, opset_version: int)`
   - `synthesize_speech(text: str, ref_audio_path: Optional[str], output_wav_path: str)`

2. **Load Pretrained Base Weights Before LoRA Wrapping**
   In `src/models/f5_adapter.py`, instantiate `DiT` (`dim=1024, depth=22, heads=16`) with `get_tokenizer("Emilia_ZH_EN", "pinyin")`. Load `model_base.safetensors` before wrapping with LoRA. Strip `ema_model.` and `transformer.` key prefixes so weights match the DiT module keys.

3. **Implement Real F5-TTS Inference Engine (`src/inference/f5_infer.py`)**
   Use `write_file` to author `synthesize_f5`:
   - Automatically pick the optimal reference audio chunk (5-9s, high confidence) from metadata via `_pick_best_ref_chunk`.
   - Load `f5_tts.model.DiT` and `vocos` 24kHz vocoder.
   - Run `infer_process` with user-specified speed and steps.
   - Apply Pedalboard DSP studio mastering (compression, EQ warmth, de-essing, subtle reverb).

4. **Add Dual-Environment Fallbacks for Headless VPS Testing**
   In `src/inference/test_checkpoint.py` and `src/models/f5_adapter.py`:
   - Wrap `synthesize_f5` imports in a try-except block.
   - On VPS environments where PyTorch or CUDA is absent, fall back gracefully to a synthetic 24kHz carrier wave with DSP mastering.
   - Maintain dual dictionary keys (`duration` and `duration_sec`, `latency_sec` and `elapsed_sec`) to prevent breaking existing test assertions.

5. **Preserve Backwards Compatibility Aliases**
   When refactoring class names or function signatures, expose legacy aliases:
   ```python
   # src/inference/engine.py
   TTSEngine = VoiceInferenceEngine

   # src/inference/test_checkpoint.py
   preview_checkpoint = preview_checkpoint_audio
   ```

6. **Bind Colab Form Parameters to CLI Arguments**
   In `notebooks/colab_pipeline.ipynb` and `src/training/finetune_lora.py`:
   - Ensure the training script accepts `--max-steps`, `--batch-size`, and `--base-weights`.
   - In Colab Cell 6.1, pass `{training_steps}` and `{batch_size}` from `#@param` form fields to prevent silent parameter ignoring.

7. **Update Colab Notebook Installation & Cells**
   Use Python JSON manipulation to update `notebooks/colab_pipeline.ipynb`:
   - Ensure Cell 1.1 includes `f5-tts vocos` in the pip install commands.
   - Update Cell 6.2 (Pre-Export Sound Check) and Cell 7.2 (Studio Voice Playground) to call `synthesize_f5` directly.

8. **Statistical Voice Evaluation Benchmark**
   Use `src.evaluation.voice_evaluator` to evaluate synthesized checkpoints:
   - Compute Cosine Similarity between generated and reference embeddings (Target > 80%).
   - Compute Thai CER/WER via Faster-Whisper ASR against prompt text (Target CER < 10%).
   - Measure F0 / Pitch mean, standard deviation, and drift percentage.
   - Calculate SNR and dynamic range in dBFS.
   - Generate Composite Quality Index (CQI Score 0-100) and render Matplotlib Radar chart.
   - Run in Colab via Cell 6.3.

9. **Execute Verification Test Suite**
   Run the test suite in `terminal`:
   ```bash
   python3 tests/test_master_pipeline.py
   ```
   Ensure all 8 tests pass with 100% success.

9. **Commit and Push Verified Code**
   Stage and push changes using `terminal`:
   ```bash
   git add -A && git commit -m "feat: real F5-TTS Flow Matching inference and CFM training integration" && git push origin main
   ```

## Pitfalls

- **Mock Stub VRAM Indicator**: If training logs show VRAM usage around ~0.06GB with step latency <15ms, the training loop is executing a dummy linear stub rather than the real F5-TTS DiT CFM model (which takes 6.5–9.5GB and 180–350ms/step on T4). See `references/finetune_diagnostics.md`.
- **Pretrained Weights Not Loaded (Blank Backbone)**: Initializing `DiT` without loading base weights causes LoRA to adapt a random neural net from scratch rather than fine-tuning speech representations.
- **EMA Tensor Key Prefix**: Official F5-TTS safetensors prefix weights with `ema_model.`. Without stripping this prefix before `load_state_dict(..., strict=False)`, PyTorch silently ignores all weights.
- **Colab UI Slider Disconnect**: Setting `#@param` form fields in Colab does not pass values to `!python -m ...` unless explicitly provided as CLI arguments.
- **Abstract Method Instantiation Failure**: Python `TypeError: Can't instantiate abstract class ... with abstract method synthesize_speech` occurs when adapter classes omit methods required by `BaseTTSAdapter`.
- **Missing Aliases**: Renaming `TTSEngine` to `VoiceInferenceEngine` without providing `TTSEngine = VoiceInferenceEngine` breaks `src/inference/__init__.py` and external callers.
- **Drive FUSE Cache Delay**: On Google Colab, files written to Google Drive by external processes may not immediately appear without calling `drive.flush_and_unmount()` or refreshing directory inodes.

## Verification

Run the pipeline verification test from the repository root:
```bash
python3 tests/test_master_pipeline.py
```
Exit code 0 with `=== ALL 7 MASTER PIPELINE TESTS PASSED WITH 100% SUCCESS RATE ===` verifies all components and fallbacks work correctly.
