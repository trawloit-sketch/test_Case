# Madura ERP / EIS — Data Migration Reconciliation Report
Generated at: 2026-10-19 08:30:32
Pipeline: Raw Extraction -> Cleaning -> Validation -> Transformation -> Staging

## Summary Metrics

| Entity | Raw Records | Accepted / Clean | Rejected / Quarantined | Clean % |
|---|---|---|---|---|
| Products | 22 | 21 | 1 | 95.5% |
| Customers | 12 | 11 | 1 | 91.7% |
| Inventory | 21 | 20 | 1 | 95.2% |
| Sales Orders | 12 | 11 | 1 | 91.7% |

## Rejection Analysis
1. **Products**: Quarantined records with negative pricing and duplicate codes.
2. **Customers**: Quarantined records with missing company name, negative credit limit, or invalid email address.
3. **Inventory**: Quarantined records with negative stock balances or invalid date formats.
4. **Sales Orders**: Quarantined records with negative quantities, discount > 50%, or invalid state transitions.

All rejected records are stored with full diagnostic audit trails in `migration/rejected/` for review during Week 13 ETL activities.
