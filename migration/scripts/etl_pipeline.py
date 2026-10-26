#!/usr/bin/env python3
"""
Madura ERP / EIS - ETL Data Migration Pipeline
Week 13 Academic Demonstration & Operational Migration Tool
Domain: Madura Salt Enterprise / MSME
"""

import os
import sys
import pandas as pd
import numpy as np
import datetime
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "raw")
CLEANED_DIR = os.path.join(BASE_DIR, "cleaned")
REJECTED_DIR = os.path.join(BASE_DIR, "rejected")

def ensure_directories():
    for d in [RAW_DIR, CLEANED_DIR, REJECTED_DIR]:
        os.makedirs(d, exist_ok=True)

def process_products():
    print("[ETL] Processing Products...")
    raw_path = os.path.join(RAW_DIR, "products.csv")
    df = pd.read_csv(raw_path)
    
    initial_count = len(df)
    rejected_rows = []
    clean_rows = []
    seen_codes = set()
    
    for idx, row in df.iterrows():
        reasons = []
        code = str(row.get('product_code', '')).strip()
        
        # Check duplicate
        if code in seen_codes:
            reasons.append("Duplicate product_code")
        seen_codes.add(code)
        
        # Check unit price
        try:
            price = float(row.get('unit_price', 0))
            if price <= 0:
                reasons.append("Unit price must be > 0")
        except:
            reasons.append("Invalid unit price format")
            
        # Check minimum stock
        try:
            min_stock = float(row.get('minimum_stock', 0))
            if min_stock < 0:
                reasons.append("Minimum stock cannot be negative")
        except:
            reasons.append("Invalid minimum stock format")
            
        if reasons:
            rejected_dict = row.to_dict()
            rejected_dict['rejection_reason'] = "; ".join(reasons)
            rejected_rows.append(rejected_dict)
        else:
            clean_rows.append(row.to_dict())
            
    df_clean = pd.DataFrame(clean_rows)
    df_rejected = pd.DataFrame(rejected_rows)
    
    df_clean.to_csv(os.path.join(CLEANED_DIR, "products_clean.csv"), index=False)
    if not df_rejected.empty:
        df_rejected.to_csv(os.path.join(REJECTED_DIR, "products_rejected.csv"), index=False)
        
    print(f" -> Products: Raw {initial_count}, Clean {len(df_clean)}, Rejected {len(df_rejected)}")
    return initial_count, len(df_clean), len(df_rejected)

def process_customers():
    print("[ETL] Processing Customers...")
    raw_path = os.path.join(RAW_DIR, "customers.csv")
    df = pd.read_csv(raw_path)
    
    initial_count = len(df)
    rejected_rows = []
    clean_rows = []
    seen_codes = set()
    
    for idx, row in df.iterrows():
        reasons = []
        code = str(row.get('customer_code', '')).strip()
        email = str(row.get('email', '')).strip()
        
        if code in seen_codes:
            reasons.append("Duplicate customer_code")
        seen_codes.add(code)
        
        if not row.get('company_name') or pd.isna(row.get('company_name')):
            reasons.append("Missing company_name")
            
        if "@" not in email or "." not in email:
            reasons.append("Invalid email address format")
            
        try:
            credit_limit = float(row.get('credit_limit', 0))
            if credit_limit < 0:
                reasons.append("Credit limit cannot be negative")
        except:
            reasons.append("Invalid credit limit")
            
        if reasons:
            rejected_dict = row.to_dict()
            rejected_dict['rejection_reason'] = "; ".join(reasons)
            rejected_rows.append(rejected_dict)
        else:
            clean_rows.append(row.to_dict())
            
    df_clean = pd.DataFrame(clean_rows)
    df_rejected = pd.DataFrame(rejected_rows)
    
    df_clean.to_csv(os.path.join(CLEANED_DIR, "customers_clean.csv"), index=False)
    if not df_rejected.empty:
        df_rejected.to_csv(os.path.join(REJECTED_DIR, "customers_rejected.csv"), index=False)
        
    print(f" -> Customers: Raw {initial_count}, Clean {len(df_clean)}, Rejected {len(df_rejected)}")
    return initial_count, len(df_clean), len(df_rejected)

def process_inventory():
    print("[ETL] Processing Inventory...")
    raw_path = os.path.join(RAW_DIR, "inventory.csv")
    df = pd.read_csv(raw_path)
    
    initial_count = len(df)
    rejected_rows = []
    clean_rows = []
    
    for idx, row in df.iterrows():
        reasons = []
        try:
            qty = float(row.get('quantity_on_hand', 0))
            if qty < 0:
                reasons.append("Quantity on hand cannot be negative")
        except:
            reasons.append("Invalid quantity format")
            
        date_str = str(row.get('last_counted_date', ''))
        try:
            datetime.date.fromisoformat(date_str)
        except:
            reasons.append("Invalid ISO date format")
            
        if reasons:
            rejected_dict = row.to_dict()
            rejected_dict['rejection_reason'] = "; ".join(reasons)
            rejected_rows.append(rejected_dict)
        else:
            clean_rows.append(row.to_dict())
            
    df_clean = pd.DataFrame(clean_rows)
    df_rejected = pd.DataFrame(rejected_rows)
    
    df_clean.to_csv(os.path.join(CLEANED_DIR, "inventory_clean.csv"), index=False)
    if not df_rejected.empty:
        df_rejected.to_csv(os.path.join(REJECTED_DIR, "inventory_rejected.csv"), index=False)
        
    print(f" -> Inventory: Raw {initial_count}, Clean {len(df_clean)}, Rejected {len(df_rejected)}")
    return initial_count, len(df_clean), len(df_rejected)

def process_sales():
    print("[ETL] Processing Sales...")
    raw_path = os.path.join(RAW_DIR, "sales.csv")
    df = pd.read_csv(raw_path)
    
    initial_count = len(df)
    rejected_rows = []
    clean_rows = []
    
    valid_statuses = {"DRAFT", "SUBMITTED", "APPROVED", "STOCK_RESERVED", "DELIVERED", "INVOICED", "PAID"}
    
    for idx, row in df.iterrows():
        reasons = []
        try:
            qty = float(row.get('quantity', 0))
            if qty <= 0:
                reasons.append("Quantity must be > 0")
        except:
            reasons.append("Invalid quantity format")
            
        try:
            disc = float(row.get('discount_percent', 0))
            if disc < 0 or disc > 50:
                reasons.append("Discount out of allowable bounds (0% - 50%)")
        except:
            reasons.append("Invalid discount format")
            
        status = str(row.get('status', '')).strip()
        if status not in valid_statuses:
            reasons.append(f"Invalid workflow status '{status}'")
            
        date_str = str(row.get('order_date', ''))
        try:
            datetime.date.fromisoformat(date_str)
        except:
            reasons.append("Invalid order date format")
            
        if reasons:
            rejected_dict = row.to_dict()
            rejected_dict['rejection_reason'] = "; ".join(reasons)
            rejected_rows.append(rejected_dict)
        else:
            clean_rows.append(row.to_dict())
            
    df_clean = pd.DataFrame(clean_rows)
    df_rejected = pd.DataFrame(rejected_rows)
    
    df_clean.to_csv(os.path.join(CLEANED_DIR, "sales_clean.csv"), index=False)
    if not df_rejected.empty:
        df_rejected.to_csv(os.path.join(REJECTED_DIR, "sales_rejected.csv"), index=False)
        
    print(f" -> Sales: Raw {initial_count}, Clean {len(df_clean)}, Rejected {len(df_rejected)}")
    return initial_count, len(df_clean), len(df_rejected)

def generate_report(metrics):
    report_path = os.path.join(BASE_DIR, "..", "docs", "migration", "reconciliation-report.md")
    report_content = f"""# Madura ERP / EIS — Data Migration Reconciliation Report
Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Pipeline: Raw Extraction -> Cleaning -> Validation -> Transformation -> Staging

## Summary Metrics

| Entity | Raw Records | Accepted / Clean | Rejected / Quarantined | Clean % |
|---|---|---|---|---|
| Products | {metrics['products'][0]} | {metrics['products'][1]} | {metrics['products'][2]} | {metrics['products'][1]/metrics['products'][0]*100:.1f}% |
| Customers | {metrics['customers'][0]} | {metrics['customers'][1]} | {metrics['customers'][2]} | {metrics['customers'][1]/metrics['customers'][0]*100:.1f}% |
| Inventory | {metrics['inventory'][0]} | {metrics['inventory'][1]} | {metrics['inventory'][2]} | {metrics['inventory'][1]/metrics['inventory'][0]*100:.1f}% |
| Sales Orders | {metrics['sales'][0]} | {metrics['sales'][1]} | {metrics['sales'][2]} | {metrics['sales'][1]/metrics['sales'][0]*100:.1f}% |

## Rejection Analysis
1. **Products**: Quarantined records with negative pricing and duplicate codes.
2. **Customers**: Quarantined records with missing company name, negative credit limit, or invalid email address.
3. **Inventory**: Quarantined records with negative stock balances or invalid date formats.
4. **Sales Orders**: Quarantined records with negative quantities, discount > 50%, or invalid state transitions.

All rejected records are stored with full diagnostic audit trails in `migration/rejected/` for review during Week 13 ETL activities.
"""
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"[ETL] Report generated at {report_path}")

def main():
    ensure_directories()
    metrics = {}
    metrics['products'] = process_products()
    metrics['customers'] = process_customers()
    metrics['inventory'] = process_inventory()
    metrics['sales'] = process_sales()
    generate_report(metrics)
    print("[ETL] Pipeline finished successfully.")

if __name__ == "__main__":
    main()
