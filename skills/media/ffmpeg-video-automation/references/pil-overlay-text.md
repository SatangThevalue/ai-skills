# Pillow (PIL) Text Overlay for FFmpeg

When `ffmpeg -vf drawtext` fails to render complex typography (such as Thai tone marks, Arabic, or complex word-wrapping), the robust alternative is to render the text to transparent PNGs using Python's `Pillow` library, and then composite them using FFmpeg's `overlay` filter.

## Python PIL Overlay Generator

```python
from PIL import Image, ImageDraw, ImageFont

def generate_text_overlay_with_mask(text_lines, font_path, font_size, image_path, width=1080, height=1920, start_y=750, line_spacing=1.8):
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, font_size)
    
    # Calculate mask bounding box to hide old burned-in video text (optional)
    total_height = int(len(text_lines) * font_size * line_spacing)
    max_width = max(d.textbbox((0, 0), line, font=font)[2] for line in text_lines)
    
    pad_x, pad_y = 40, 20
    rect_x0 = (width - max_width) / 2 - pad_x
    rect_y0 = start_y - pad_y
    rect_x1 = rect_x0 + max_width + (pad_x*2)
    rect_y1 = start_y + total_height + pad_y
    
    d.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill=(0, 0, 0, 255)) # Solid black mask
    
    current_y = start_y
    for line in text_lines:
        text_width = d.textbbox((0, 0), line, font=font)[2]
        x_pos = (width - text_width) / 2
        
        # Shadow
        d.text((x_pos+4, current_y+4), line, font=font, fill=(0, 0, 0, 255))
        # Main text
        d.text((x_pos, current_y), line, font=font, fill=(255, 255, 255, 255))
        
        current_y += int(font_size * line_spacing) 
    
    img.save(image_path)
```

## FFmpeg Chained Overlay Execution

To apply multiple overlays sequentially (e.g., subtitles appearing at different times), you must chain the `overlay` filter outputs.

```bash
ffmpeg -y -i input.mp4 \
-i overlay_1.png -i overlay_2.png \
-filter_complex "[0:v]scale=-1:1920,crop=1080:1920[bg]; \
                 [1:v]format=rgba[ol1]; [2:v]format=rgba[ol2]; \
                 [bg][ol1]overlay=0:0:enable='between(t,0,5)'[v1]; \
                 [v1][ol2]overlay=0:0:enable='between(t,5,10)'[outv]" \
-map "[outv]" -map 0:a -c:v libx264 -preset fast -crf 23 -c:a aac -t 10 output.mp4
```