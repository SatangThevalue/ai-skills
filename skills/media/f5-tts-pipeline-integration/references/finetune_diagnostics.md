# F5-TTS Fine-Tuning & Diagnostic Reference

## 1. Training Signature: Mock vs. Real F5-TTS DiT

When diagnosing Colab training logs, compare against these benchmark metrics on an NVIDIA T4 (15GB VRAM):

| Metric | Mock / Linear Stub | Real Pretrained F5-TTS DiT (LoRA) |
|---|---|---|
| **Allocated VRAM** | 0.03 – 0.06 GB | **6.5 – 9.5 GB** |
| **Reserved VRAM** | 0.06 GB | **8.0 – 11.5 GB** |
| **Step Latency** | 3.8 – 12 ms | **180 – 350 ms** (batch_size=2) |
| **Loss Behavior** | Fluctuate flat ~0.90 – 1.05 | Descends steadily: 1.5+ down to 0.35 – 0.50 |
| **Backpropagation** | `dummy_in` MSE loss | Conditional Flow Matching (CFM) vector field MSE |

---

## 2. Pretrained Base Weights & EMA Prefix Stripping

Upstream F5-TTS checkpoints (`model_1200000.safetensors` or `model_1200000.pt`) store weights with EMA prefixes. Directly loading them into a clean `DiT` instance with `strict=False` silently ignores all keys, leaving the backbone randomly initialized.

```python
from safetensors.torch import load_file
import torch

def load_f5_base_weights(dit_model: torch.nn.Module, ckpt_path: str):
    if ckpt_path.endswith(".safetensors"):
        state_dict = load_file(ckpt_path)
    else:
        state_dict = torch.load(ckpt_path, map_location="cpu")

    clean_state = {}
    for k, v in state_dict.items():
        clean_k = k
        if clean_k.startswith("ema_model."):
            clean_k = clean_k[len("ema_model."):]
        if clean_k.startswith("transformer."):
            clean_k = clean_k[len("transformer."):]
        clean_state[clean_k] = v

    missing, unexpected = dit_model.load_state_dict(clean_state, strict=False)
    # Expected: 0 missing base weights
    return missing, unexpected
```

---

## 3. Tokenizer Compatibility

The official `F5TTS_Base` embedding table is trained on:
```python
from f5_tts.model.utils import get_tokenizer

vocab_char_map, vocab_size = get_tokenizer("Emilia_ZH_EN", "pinyin")
```
- Calling `get_tokenizer("custom", "custom")` without an explicit custom `vocab.txt` path produces embedding size mismatches.
- Input text to CFM forward pass should be normalized text strings (`batch["texts"]`).

---

## 4. Colab Form to CLI Binding Pattern

Colab `#@param` form fields define Python variables in the notebook kernel. Calling a Python module via `!python -m ...` starts a separate OS subprocess that cannot see kernel variables unless explicitly passed as CLI arguments:

```python
# Colab UI Cell
train_speaker = "satang" #@param {type:"string"}
training_steps = 2500 #@param {type:"integer"}
batch_size = 2 #@param {type:"integer"}

# Correct Subprocess Invocation
!python -m src.training.finetune_lora \
    --config configs/base_config.yaml \
    --lora-config configs/lora_config.yaml \
    --speaker-id "{train_speaker}" \
    --max-steps {training_steps} \
    --batch-size {batch_size} \
    --base-weights "/content/drive/MyDrive/tts-project/00_base_models/f5-tts/model_base.safetensors"
```
