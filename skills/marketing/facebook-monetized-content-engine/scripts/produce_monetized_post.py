#!/usr/bin/env python3
"""
Produce Monetized Post Helper
Connects to Satang Content Studio pipeline to execute next multi-slot content item.
"""
import sys
import os

sys.path.insert(0, "/home/thaieasyvps/satang_content_studio")
sys.path.insert(0, "/home/thaieasyvps")

try:
    from studio_pipeline import produce_monetized_content
    result = produce_monetized_content()
    if result:
        print(f"[SUCCESS] Produced Eval #{result['evaluation_id']} ({result['headline']}) -> {result['gdrive_file_name']}")
        sys.exit(0)
    else:
        print("[NOTICE] No pending planned items to produce.")
        sys.exit(0)
except Exception as e:
    print(f"[ERROR] Pipeline execution failed: {e}")
    sys.exit(1)
