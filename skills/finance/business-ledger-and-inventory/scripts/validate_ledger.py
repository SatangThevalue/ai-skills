import sys
import csv
from datetime import datetime

def validate_coa(coa_path):
    print(f"[*] Validating COA: {coa_path}")
    errors = []
    try:
        with open(coa_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Check headers
            required_fields = ['account_code', 'account_name_th', 'account_name_en', 'category', 'type']
            for field in required_fields:
                if field not in reader.fieldnames:
                    errors.append(f"Missing required field in COA header: {field}")
            
            codes = set()
            for line_no, row in enumerate(reader, start=2):
                code = row.get('account_code')
                name_th = row.get('account_name_th')
                category = row.get('category')
                
                if not code or not code.isdigit():
                    errors.append(f"Line {line_no}: Invalid or missing account_code: '{code}'")
                else:
                    if code in codes:
                        errors.append(f"Line {line_no}: Duplicate account_code: {code}")
                    codes.add(code)
                    
                    # Verify 5 category rules
                    first_digit = int(code[0])
                    expected_map = {
                        1: "Asset",
                        2: "Liability",
                        3: "Equity",
                        4: "Revenue",
                        5: "Expense"
                    }
                    if first_digit in expected_map:
                        if category != expected_map[first_digit]:
                            errors.append(f"Line {line_no}: Code {code} starts with {first_digit} so category must be '{expected_map[first_digit]}', got '{category}'")
                    else:
                        errors.append(f"Line {line_no}: Account code {code} must start with 1-5 (5 main categories)")
                
                if not name_th:
                    errors.append(f"Line {line_no}: Missing account_name_th")
    except Exception as e:
        errors.append(f"COA File reading error: {str(e)}")
    
    return errors

def validate_journal(journal_path, coa_codes):
    print(f"[*] Validating Journal entries: {journal_path}")
    errors = []
    try:
        with open(journal_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            required_fields = ['entry_id', 'date', 'ref_no', 'account_code', 'dr_cr', 'amount_satang']
            for field in required_fields:
                if field not in reader.fieldnames:
                    errors.append(f"Missing required field in Journal header: {field}")
            
            entries = {}
            for line_no, row in enumerate(reader, start=2):
                entry_id = row.get('entry_id')
                date_str = row.get('date')
                code = row.get('account_code')
                dr_cr = row.get('dr_cr')
                amount_str = row.get('amount_satang')
                
                # Check date
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    errors.append(f"Line {line_no}: Date '{date_str}' is not in YYYY-MM-DD format")
                
                # Check account code exists in COA
                if code not in coa_codes:
                    errors.append(f"Line {line_no}: Account code '{code}' does not exist in Chart of Accounts")
                
                # Check Dr/Cr
                if dr_cr not in ['Dr', 'Cr']:
                    errors.append(f"Line {line_no}: dr_cr must be 'Dr' or 'Cr', got '{dr_cr}'")
                
                # Check amount_satang is integer
                try:
                    amount = int(amount_str)
                    if amount < 0:
                        errors.append(f"Line {line_no}: amount_satang must be non-negative, got {amount}")
                except ValueError:
                    errors.append(f"Line {line_no}: amount_satang must be an integer, got '{amount_str}'")
                
                # Group for double-entry check (Dr total must equal Cr total per entry_id)
                if entry_id not in entries:
                    entries[entry_id] = {'dr': 0, 'cr': 0}
                
                try:
                    val = int(amount_str)
                    if dr_cr == 'Dr':
                        entries[entry_id]['dr'] += val
                    elif dr_cr == 'Cr':
                        entries[entry_id]['cr'] += val
                except ValueError:
                    pass
            
            # Verify double-entry match
            for eid, balances in entries.items():
                if balances['dr'] != balances['cr']:
                    errors.append(f"Entry ID {eid} unbalanced: Total Debit = {balances['dr']} satang, Total Credit = {balances['cr']} satang. Diff = {abs(balances['dr'] - balances['cr'])}")
                    
    except Exception as e:
        errors.append(f"Journal File reading error: {str(e)}")
    
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 validate_ledger.py <coa.csv> <journal.csv>")
        sys.exit(1)
        
    coa_file = sys.argv[1]
    journal_file = sys.argv[2]
    
    coa_errors = validate_coa(coa_file)
    if coa_errors:
        print("\n[!] CHART OF ACCOUNTS VALIDATION ERRORS FOUND:")
        for err in coa_errors:
            print(f"  - {err}")
    else:
        print("[+] Chart of Accounts is VALID!")
        
    # Get valid codes for checking
    valid_codes = set()
    try:
        with open(coa_file, mode='r', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                valid_codes.add(r['account_code'])
    except Exception:
        pass
        
    journal_errors = validate_journal(journal_file, valid_codes)
    if journal_errors:
        print("\n[!] JOURNAL VALIDATION ERRORS FOUND:")
        for err in journal_errors:
            print(f"  - {err}")
    else:
        print("[+] Journal entries are VALID and balanced!")
        
    if coa_errors or journal_errors:
        sys.exit(1)
    else:
        print("\n[+] All financial validation checks passed successfully!")
        sys.exit(0)
