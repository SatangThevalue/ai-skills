# Scripts and utilities for Thai Personal Accounting and Finance Validation

import json

def calculate_ratios(liquid_assets, monthly_expenses, savings_investment, total_income, debt_payment, total_debt, total_assets, active_income, passive_income):
    """
    Calculate personal financial ratios based on Stock Exchange of Thailand (SET) Happy Money standards.
    """
    results = {}
    
    # 1. Basic Liquidity Ratio
    results['basic_liquidity_ratio'] = liquid_assets / monthly_expenses if monthly_expenses > 0 else 0
    results['basic_liquidity_ok'] = 3.0 <= results['basic_liquidity_ratio'] <= 6.0
    
    # 2. Saving Ratio
    results['saving_ratio'] = (savings_investment / total_income) * 100 if total_income > 0 else 0
    results['saving_ok'] = results['saving_ratio'] >= 10.0
    
    # 3. Debt Service Ratio (DSR)
    results['debt_service_ratio'] = (debt_payment / total_income) * 100 if total_income > 0 else 0
    results['debt_service_ok'] = results['debt_service_ratio'] <= 45.0 # Max 35-45%
    
    # 4. Debt to Asset Ratio
    results['debt_to_asset_ratio'] = (total_debt / total_assets) * 100 if total_assets > 0 else 0
    results['debt_to_asset_ok'] = results['debt_to_asset_ratio'] <= 50.0
    
    # 5. Survival Ratio
    results['survival_ratio'] = (active_income + passive_income) / monthly_expenses if monthly_expenses > 0 else 0
    results['survival_ok'] = results['survival_ratio'] >= 1.0
    
    # 6. Wealth Ratio
    results['wealth_ratio'] = passive_income / monthly_expenses if monthly_expenses > 0 else 0
    results['wealth_ok'] = results['wealth_ratio'] >= 1.0
    
    return results

if __name__ == '__main__':
    # Test sample with normal financial health
    # Assume 30,000 THB income, 15,000 expenses, 5,000 saving, 60,000 liquid assets, 3,000 debt payment, 150,000 total debt, 500,000 total assets.
    sample = {
        "liquid_assets": 60000.0,
        "monthly_expenses": 15000.0,
        "savings_investment": 5000.0,
        "total_income": 30000.0,
        "debt_payment": 3000.0,
        "total_debt": 150000.0,
        "total_assets": 500000.0,
        "active_income": 28000.0,
        "passive_income": 2000.0
    }
    
    ratios = calculate_ratios(**sample)
    print(json.dumps(ratios, indent=2))
