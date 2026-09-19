# Nassau Candy Distributor — Analytical Report

## Executive finding
The dataset supports descriptive analysis and a reproducible predictive benchmark, but it does not support a validated causal claim that moving a product to another factory will improve shipping performance.

## Data audit
- 10,194 rows
- 18 raw columns
- 8,549 unique orders
- 15 products
- 0 missing cells
- 0 duplicate rows
- Gross Profit is consistent with Sales minus Cost to floating-point precision.

## Date quality
Order dates run from 2024-01-02 through 2025-12-31. Ship dates run from 2026-06-30 through 2030-06-28. Recorded lead time is 904–1,642 days with median 1,274 days.

## Predictive benchmark
Gradient Boosting: MAE 162.59, RMSE 177.77, R² 0.040.
Linear Regression: MAE 180.41, RMSE 182.13, R² -0.007.
Random Forest: MAE 163.47, RMSE 183.86, R² -0.026.

## Factory optimization
Each product has one supplied historical factory. Alternative-factory scores are therefore model-based counterfactual proxies, not observed intervention effects.

## Financial analysis
Historical Sales, Cost and Gross Profit are available. Incremental reassignment profit is unavailable because transportation, reassignment and factory-specific production costs are absent.

## Recommended next data
Corrected shipment timestamps, historical factory assignments, factory capacity/utilization, transportation cost, production cost/lead time, inventory availability, destination coordinates and reassignment constraints.
