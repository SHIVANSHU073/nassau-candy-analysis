# Nassau Candy Distributor — Analysis

Reusable analytical code for factory reallocation and shipping optimization.

## Scope
This repository contains data audit, cleaning, EDA, feature engineering, predictive modeling, clustering, scenario simulation, optimization logic, analytical outputs and documentation. It does **not** contain the raw customer/order CSV.

## Current data caveats
The supplied order/ship dates generate recorded intervals of 904–1,642 days. These values are preserved but are not treated as verified physical shipping transit times.

The supplied product-to-factory mapping gives each product one factory, so alternative-factory effects are not historically identified. Counterfactual factory outputs are therefore labelled simulations/model proxies.

## Reproduce locally
1. Place the supplied CSV in `data/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run: `python run_analysis.py --csv data/<filename>.csv`.

## Package
The `src/nassau_analysis` package is intended to be consumed by the separate Streamlit repository.

## Public-data rule
Never commit the supplied raw CSV or private customer-level data.

## Deployment note
The original serialized Gradient Boosting deployment artifact was corrupted and has been removed from the public package. The Streamlit app now detects an unavailable binary model and uses a deterministic historical baseline proxy instead of failing or fabricating a factory effect. The benchmark metrics in `model_metrics.csv` remain unchanged and are the evaluation results from the analytical workflow.
