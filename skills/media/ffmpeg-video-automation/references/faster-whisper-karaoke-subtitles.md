# Faster-Whisper Subtitle Engine for Video Automation

Using `faster-whisper` allows extracting word-level timestamps on a VPS CPU very quickly, outputting `.ass` for dynamic karaoke effects.

## The Recipe

```python
from faster_whisper import WhisperModel

MODEL_SIZE = "base" 
DEVICE = "cpu"
COMPUTE_TYPE = "int8"

model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
segments, info = model.transcribe(audio_path, beam_size=5, word_timestamps=True)

# Generate Advanced SubStation Alpha (.ass) format for styling
ass_events = []
for segment in segments:
    for word_info in segment.words:
        start_time = format_timestamp(word_info.start) # Convert seconds to H:MM:SS.cs
        end_time = format_timestamp(word_info.end)
        text = word_info.word.strip()
        
        # Override tags for styling (e.g., yellow hex color in BGR format &H00FFFF&)
        styled_text = f"{{\\c&H00FFFF&}}{text}" 
        
        # Bottom-Center alignment is 2.
        ass_line = f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{styled_text}\\n"
        ass_events.append(ass_line)
```

## Best Practices
* Use the **`base`** or **`tiny`** model for English TTS audio as the enunciation is perfect, requiring very little compute.
* Use the **`small`** or **`medium`** model for Thai, as Thai lacks spaces between words and requires better semantic models for word-boundary detection.
* `int8` quantization dramatically reduces RAM footprint.