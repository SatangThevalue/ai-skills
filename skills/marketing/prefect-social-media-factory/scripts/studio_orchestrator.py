#!/usr/bin/env python3
"""
Prefect Social Media Factory : Master Orchestrator CLI Helper
Provides quick commands to test and trigger factory pipelines:
- python3 studio_orchestrator.py morning-briefing
- python3 studio_orchestrator.py harvest-pantip
- python3 studio_orchestrator.py harvest-open-apis
- python3 studio_orchestrator.py sweep-publisher
"""
import sys
import subprocess

SCRIPTS = {
    "morning-briefing": "/home/thaieasyvps/satang_content_studio/prefect_morning_briefing.py",
    "harvest-pantip": "/home/thaieasyvps/satang_content_studio/satang_prefect_pantip_harvester.py",
    "harvest-open-apis": "/home/thaieasyvps/satang_content_studio/satang_prefect_open_apis_harvester.py",
    "sweep-publisher": "/home/thaieasyvps/satang_prefect_sweeper.py",
    "produce-next": "/home/thaieasyvps/satang_content_studio/studio_pipeline.py"
}

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SCRIPTS:
        print("Usage: python3 studio_orchestrator.py <command>")
        print("Available commands:", list(SCRIPTS.keys()))
        sys.exit(1)

    cmd_name = sys.argv[1]
    target_script = SCRIPTS[cmd_name]
    print(f"[ORCHESTRATOR] Triggering {cmd_name} ({target_script})...")
    res = subprocess.run(["python3", target_script])
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
