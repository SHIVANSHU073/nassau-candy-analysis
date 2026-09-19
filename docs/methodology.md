# Analytical Methodology

## Data preparation
Schema/type validation, missing-value checks, duplicate checks, category normalization, date parsing, financial consistency and product-factory reference joining.

## Target
`recorded_lead_time_days = Ship Date - Order Date`. The supplied dates produce 904–1,642 day intervals, so the target is explicitly qualified as a recorded dataset interval.

## Predictive models
- Linear Regression baseline
- Random Forest Regressor
- Gradient Boosting Regressor

Primary validation uses a chronological 80/20 split with MAE, RMSE and R².

## Clustering
Product/factory/region/ship-mode segments are aggregated and standardized. K-Means candidates are evaluated using silhouette score.

## Simulation
Alternative-factory scenarios replace the factory category in model inputs. Because historical within-product factory variation is absent, these are model-based counterfactual proxies rather than causal estimates.

## Optimization
Transparent scoring combines normalized lead-time improvement, financial exposure and risk. Missing capacity and cost constraints prevent claims of operational feasibility.
