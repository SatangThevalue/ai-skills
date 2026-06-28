import sys

def calculate_personal_tax(net_income):
    brackets = [
        (150000, 0.00),
        (300000, 0.05),
        (500000, 0.10),
        (750000, 0.15),
        (1000000, 0.20),
        (2000000, 0.25),
        (5000000, 0.30),
        (float('inf'), 0.35)
    ]
    
    tax = 0
    previous_limit = 0
    remaining = net_income
    
    for limit, rate in brackets:
        bracket_size = limit - previous_limit
        if remaining > bracket_size:
            tax += bracket_size * rate
            remaining -= bracket_size
            previous_limit = limit
        else:
            tax += remaining * rate
            break
            
    return tax

def calculate_corporate_sme_tax(net_profit):
    # SME Corporate Tax: Capital <= 5M and Revenue <= 30M
    if net_profit <= 300000:
        return 0
    elif net_profit <= 3000000:
        return (net_profit - 300000) * 0.15
    else:
        return (3000000 - 300000) * 0.15 + (net_profit - 3000000) * 0.20

if __name__ == '__main__':
    # Test sample calculation: Net Income / Net Profit of 1.5 million THB
    test_val = 1500000
    p_tax = calculate_personal_tax(test_val)
    c_tax = calculate_corporate_sme_tax(test_val)
    print(f"Net Income/Profit: {test_val:,.2f} THB")
    print(f"Personal Income Tax: {p_tax:,.2f} THB")
    print(f"SME Corporate Tax: {c_tax:,.2f} THB")
    print(f"Difference (Potential Saving): {p_tax - c_tax:,.2f} THB")
