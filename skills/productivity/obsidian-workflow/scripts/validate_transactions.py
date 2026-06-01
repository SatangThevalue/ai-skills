#!/usr/bin/env python3
"""
Validator for transactions.csv shipped with obsidian-workflow skill.
Checks schema, integer amount_cents, ISO date in 'date' or 'created_at', and prints totals.
"""
import csv
import sys
from pathlib import Path
from datetime import datetime

PATH = Path('transactions.csv')
if not PATH.exists():
    print('transactions.csv not found in current directory')
    sys.exit(1)

with PATH.open() as f:
    reader = csv.DictReader(f)
    expected = ['id','date','account','counterparty','category','amount_cents','currency','type','tags','notes','source_file','created_at']
    if reader.fieldnames != expected:
        print('Header mismatch. Expected:', expected)
        print('Found:', reader.fieldnames)
        # continue but warn
    total = 0
    rows = list(reader)
    for r in rows:
        try:
            amt = int(r.get('amount_cents','0') or 0)
        except Exception:
            print('Invalid amount_cents in row:', r)
            raise
        date_str = r.get('date') or r.get('created_at')
        if date_str:
            try:
                datetime.fromisoformat(date_str)
            except Exception:
                print('Invalid date format:', date_str)
        total += amt

print('Rows:', len(rows))
print('Total amount_cents:', total)
