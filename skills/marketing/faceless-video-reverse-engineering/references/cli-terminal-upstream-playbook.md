# CLI Terminal Tech Explainer Upstream Playbook

Guidelines and patterns for converting raw upstream developer documentation into viral 9:16 terminal animations.

## Upstream Data Extraction Pattern

1. **Harvest Primary Documentation**:
   - Query official LLM-friendly documentation endpoints first (e.g. `https://<domain>/docs/llms.txt`).
   - Extract raw CLI reference tables, command-line flags, configuration hierarchies, and diagnostic subcommands.
   - Look specifically for hidden subcommands, aliases, and safety defaults that developers struggle with.

2. **The 4-Beat Storytelling Spine**:
   - **Beat 1: The Hook & Alias (0.0s - 6.0s)**
     - macOS terminal typing animation (`> /command`)
     - Immediate reveal of the official alias (e.g., `> /checkup`)
     - White floating documentation pill card with official source link
   - **Beat 2: The Deep Checklist (6.0s - 12.0s)**
     - 4 numbered checklist cards (`01` to `04`)
     - Balanced right-side status pills on every row
   - **Beat 3: Safety & Human-in-the-Loop Principle (12.0s - 17.5s)**
     - Big bold statement (e.g., "Zero Silent Mutations!", "มันไม่แก้ให้เงียบๆ!")
     - Warning box highlighting developer confirmation (`[y/N]`)
   - **Beat 4: Standalone Rescue Mode (17.5s - 23.0s)**
     - OS terminal prompt (`bash$ claude doctor`)
     - Status badges: `[พิมพ์ที่ terminal ตรงๆ]`, `[Read-Only Diagnostics]`
     - Callout on when to use: when the primary session fails to launch.

## Visual Design & Typography Rules

- **Balanced List Badges**:
  Never put an alert tag on only one card in a list. If card 04 has `<span class="tag-danger">กิน Context</span>`, cards 01-03 must also feature status badges (e.g. `<span class="tag-orange">ชนกัน</span>`, `<span class="tag-orange">หาไม่พบ</span>`, `<span class="tag-orange">ฟอร์แมตพัง</span>`).
- **Language Uniformity**:
  Maintain language consistency across badge rows. Use `ฟอร์แมตพัง` instead of `syntax error` when the surrounding cards use Thai status tags.
- **Fast Card Stagger**:
  In short 20s Reels, stagger card entrances quickly (`0.3s - 0.4s` apart, starting at scene onset). All 4 cards must be on screen within 1.5 seconds of the beat starting to give viewers sufficient reading time.
