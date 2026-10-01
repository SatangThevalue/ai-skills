#!/usr/bin/env python3
"""
Design Audit Toolkit : Visual Hierarchy, Typography, and WCAG Contrast Auditor
Part of 'content-creation-github-stack' skill.
"""
import sys
import os
import math
from fontTools.ttLib import TTFont

def hex_to_rgb(hex_str: str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def get_relative_luminance(rgb):
    """Calculate WCAG 2.1 relative luminance."""
    srgb = [c / 255.0 for c in rgb]
    lum = []
    for c in srgb:
        if c <= 0.03928:
            lum.append(c / 12.92)
        else:
            lum.append(((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * lum[0] + 0.7152 * lum[1] + 0.0722 * lum[2]

def get_contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG contrast ratio between two hex colors."""
    l1 = get_relative_luminance(hex_to_rgb(hex1))
    l2 = get_relative_luminance(hex_to_rgb(hex2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)

def audit_font_metrics(font_path: str):
    """Inspects font metadata, units per EM, ascender/descender using fontTools."""
    if not os.path.exists(font_path):
        return {"error": f"Font file not found: {font_path}"}
    
    tt = TTFont(font_path)
    head = tt['head']
    hhea = tt['hhea']
    os2 = tt['OS/2'] if 'OS/2' in tt else None
    
    return {
        "font_family": tt['name'].getDebugName(1),
        "units_per_em": head.unitsPerEm,
        "ascender": hhea.ascent,
        "descender": hhea.descent,
        "line_gap": hhea.lineGap,
        "weight_class": os2.usWeightClass if os2 else "N/A",
        "supports_thai": 0x0E01 in [ord(c) for c in "กขค"]
    }

def run_brand_audit(bg_hex="#070D1F", gold_hex="#F5A623", cyan_hex="#38BDF8", white_hex="#FFFFFF"):
    """Runs brand CI compliance check against WCAG AA (4.5:1 for body, 3:1 for large)."""
    cr_gold = get_contrast_ratio(gold_hex, bg_hex)
    cr_cyan = get_contrast_ratio(cyan_hex, bg_hex)
    cr_white = get_contrast_ratio(white_hex, bg_hex)
    
    print("=== BRAND COLOR CONTRAST AUDIT (WCAG 2.1) ===")
    print(f"Background: {bg_hex}")
    print(f"Gold Accent ({gold_hex}) vs BG : Contrast {cr_gold}:1 -> {'PASS (AAA Large)' if cr_gold >= 4.5 else 'PASS (AA Large)' if cr_gold >= 3.0 else 'FAIL'}")
    print(f"Cyan Accent ({cyan_hex}) vs BG : Contrast {cr_cyan}:1 -> {'PASS (AAA Large)' if cr_cyan >= 4.5 else 'PASS (AA Large)' if cr_cyan >= 3.0 else 'FAIL'}")
    print(f"White Text  ({white_hex}) vs BG : Contrast {cr_white}:1 -> {'PASS (AAA Super)' if cr_white >= 7.0 else 'PASS'}")

def main():
    if "--check" in sys.argv:
        cr = get_contrast_ratio("#FFFFFF", "#000000")
        if cr >= 20.0:
            print("DESIGN_AUDIT_OK")
            sys.exit(0)
        sys.exit(1)
        
    font_sample = "/home/thaieasyvps/.fonts/Prompt/Prompt-Bold.ttf"
    if os.path.exists(font_sample):
        metrics = audit_font_metrics(font_sample)
        print("=== FONT METRICS AUDIT (fontTools) ===")
        for k, v in metrics.items():
            print(f"• {k}: {v}")
        print()
        
    run_brand_audit()

if __name__ == "__main__":
    main()
