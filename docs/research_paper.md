# Data-Driven Factory Allocation and Shipping Lead-Time Analysis for Nassau Candy Distribution

**Author:** Shivanshu  
**Project:** Nassau Candy Distributor — Data Analysis and Streamlit Decision-Support System  
**Repository:** `SHIVANSHU073/nassau-candy-analysis`

## Abstract

This study develops a data-driven analytical framework for examining shipping lead time, product behavior, regional patterns, and factory-allocation scenarios for a candy distribution dataset. The dataset contains 10,194 shipment records covering 8,549 unique orders, 15 products, and multiple regions, shipping modes, and manufacturing factories. The analysis follows a reproducible workflow consisting of data auditing, cleaning, exploratory analysis, feature engineering, supervised learning, clustering, scenario simulation, and optimization-oriented decision support.

Recorded lead time was calculated as the difference between ship date and order date. Its observed range was 904 to 1,642 days, with a median of 1,274 days. Three regression models—Linear Regression, Random Forest, and Gradient Boosting—were evaluated using a chronological 80/20 train-test split. Gradient Boosting produced the lowest test MAE among the evaluated models (162.586 days), with RMSE of 177.767 days and R² of 0.040. The low R² indicates that the available variables explain only a small proportion of observed lead-time variation, so model outputs should be treated as predictive scenarios rather than causal estimates.

A key structural limitation is that factory assignment is confounded with product assignment: the dataset does not provide sufficient within-product factory variation to separately estimate a factory effect. Consequently, the project avoids claiming that a particular factory will causally reduce lead time. Instead, the deployed Streamlit application distinguishes historical observations from model-based scenario estimates and uses a historical baseline proxy when the serialized model artifact is unavailable. The resulting system provides an auditable foundation for exploratory supply-chain analysis while clearly communicating uncertainty and data limitations.

**Keywords:** supply chain analytics, factory allocation, shipping lead time, machine learning, Gradient Boosting, clustering, scenario analysis, Streamlit, decision support

## 1. Introduction

Supply-chain decisions frequently require organizations to understand why orders experience different fulfillment times and how operational scenarios might affect service performance. Historical transaction data can provide useful evidence about patterns across products, regions, shipping modes, time periods, and manufacturing locations. However, observational data must be interpreted carefully because associations in historical records do not automatically establish causal effects.

This project studies a Nassau Candy Distributor shipment dataset with the objective of building a reproducible analytical and decision-support workflow. The work combines descriptive analytics with predictive modeling and scenario simulation. The final output is a Streamlit application designed to make the analysis accessible through interactive views of data quality, model performance, factory scenarios, what-if analysis, and recommendations.

The study addresses five questions:

1. What are the principal characteristics and quality issues in the shipment dataset?
2. How does recorded shipping lead time vary across products, regions, shipping modes, and time?
3. How accurately can the available historical variables predict recorded lead time?
4. What customer or shipment segments can be identified from the available data?
5. How can factory-allocation scenarios be presented without overstating what the observational data can identify?

## 2. Dataset and Data Preparation

The analytical dataset contains **10,194 rows and 21 columns**. There are **10,194 unique row identifiers** and **8,549 unique order identifiers**, covering **15 products**. The audit found no missing cells and no duplicate rows.

Order dates range from **2024-01-02 to 2025-12-31**, while ship dates range from **2026-06-30 to 2030-06-28**. Recorded lead time is defined as:

$$
LeadTime_i = ShipDate_i - OrderDate_i
$$

The observed lead-time range is **904–1,642 days**, with a median of **1,274 days**.

Gross profit consistency was also checked against the relevant revenue and cost fields; the maximum numerical discrepancy was approximately **7 × 10⁻¹⁵**, consistent with floating-point precision.

The workflow includes product-to-factory mapping, factory coordinates, region information, shipping-mode information, and derived temporal variables. No unmatched products were found in the product-to-factory mapping.

The raw CSV is intentionally excluded from the public repository through Git ignore rules. Reproducibility is supported through documented transformations, summary files, notebooks, and the reusable Python package.

## 3. Methodology

### 3.1 Exploratory Data Analysis

Exploratory analysis examines:

- product-level order and lead-time behavior;
- regional differences;
- shipping-mode distributions;
- factory assignments and geographic coordinates;
- temporal patterns;
- gross profit and quantity-related variables;
- distributions and potential outliers.

Descriptive summaries are used to identify patterns before predictive or optimization-oriented analysis is performed.

### 3.2 Feature Engineering

Features were constructed from the historical transaction fields and include product, regional, shipping-mode, temporal, quantity, sales/profit, and related operational attributes where available.

Categorical variables were encoded for modeling. Temporal ordering was preserved for evaluation to reduce leakage from future observations into training data.

### 3.3 Predictive Modeling

Three regression approaches were benchmarked:

- Linear Regression
- Random Forest Regression
- Gradient Boosting Regression

The dataset was divided chronologically using an **80/20 train-test split**. This approach is more appropriate for a time-ordered operational dataset than a purely random split when the objective is to estimate performance on later observations.

Performance was evaluated using Mean Absolute Error (MAE), Root Mean Squared Error (RMSE), and coefficient of determination (R²).

### 3.4 Clustering

Unsupervised clustering was used to investigate whether observations form meaningful groups based on selected analytical features. Candidate values of (k) from 2 through 6 were compared using silhouette scores.

Observed silhouette scores were approximately:

| Number of clusters | Silhouette score |
|---:|---:|
| 2 | 0.614 |
| 3 | 0.517 |
| 4 | 0.541 |
| 5 | 0.503 |
| 6 | 0.487 |

The clustering analysis is exploratory and is not interpreted as proof of naturally occurring business segments.

### 3.5 Scenario Simulation

Scenario analysis changes selected input conditions and generates estimated lead-time outcomes. The application distinguishes:

- historical observed values;
- predictive model estimates;
- scenario/counterfactual estimates;
- historical baseline proxy estimates.

This distinction is important because a predictive model trained on observational data should not automatically be interpreted as a causal simulation of changing factory assignment.

### 3.6 Optimization-Oriented Analysis

The project investigates factory reallocation as a decision-support problem. However, the available dataset does not contain sufficient information about factory capacity, transportation cost, production constraints, or within-product variation across factories.

Therefore, the optimization layer is framed as scenario analysis rather than a mathematically definitive production-allocation plan.

## 4. Results

### 4.1 Predictive Performance

The chronological test-set results were:

| Model | MAE (days) | RMSE (days) | R² |
|---|---:|---:|---:|
| Linear Regression | 180.414 | 182.133 | -0.007 |
| Random Forest | 163.466 | 183.862 | -0.026 |
| Gradient Boosting | 162.586 | 177.767 | 0.040 |

Among the evaluated models, Gradient Boosting produced the smallest MAE and RMSE and was therefore selected as the benchmark model for the analytical comparison.

However, its R² of approximately 0.04 indicates weak explanatory power. The model should therefore be understood as a limited predictive benchmark rather than a high-confidence forecasting system.

### 4.2 Factory Assignment and Identifiability

An important finding is that **factory assignment is confounded with product assignment**. The available data do not contain adequate within-product factory variation to estimate a separate factory effect.

For example, if a product is historically associated with one factory only, then a model cannot reliably distinguish whether observed lead time is caused by the factory, the product, or other correlated characteristics. This is an identification problem rather than simply a model-selection problem.

As a result, the analysis does not claim that moving a product to another factory would produce a specific causal lead-time reduction.

### 4.3 Deployment Robustness

The project is implemented as two public repositories:

1. an analysis/package repository containing the analytical workflow and reusable package;
2. a Streamlit repository containing the interactive decision-support application.

The application includes a deployment fallback. If the serialized Gradient Boosting artifact cannot be loaded, the system uses a deterministic historical baseline proxy constructed from product, region, and shipping-mode summaries. The fallback explicitly avoids fabricating factory-specific effects.

## 5. Discussion

The results demonstrate the usefulness and limitations of applying machine learning to operational shipment data.

First, the dataset contains substantial recorded lead-time variation. This makes predictive analysis relevant, but the relatively low R² values indicate that the available variables do not capture most of the variation. Additional operational variables would be required for a stronger predictive system.

Second, chronological evaluation is important. Randomly mixing earlier and later transactions could make a model appear more accurate than it would be when applied to future operations.

Third, factory optimization cannot be treated as an ordinary feature-importance exercise. Because product and factory assignments are structurally linked in the available observations, the data do not provide a clean experimental or quasi-experimental basis for estimating the effect of changing factories.

Fourth, scenario analysis can still be useful when presented transparently. A decision-support interface can show what the historical data and predictive model imply under specified inputs while clearly identifying which outputs are estimates rather than observed outcomes.

## 6. Limitations

Several limitations should be considered before using the results for operational decisions:

1. **Observational data:** The dataset records historical operations rather than randomized factory assignments.
2. **Factory-product confounding:** There is insufficient within-product factory variation for reliable factory-effect estimation.
3. **Missing operational constraints:** Factory capacity, production limits, transportation costs, inventory levels, and service-level constraints are not available.
4. **Weak predictive fit:** The benchmark model has an R² of approximately 0.04 on the chronological test set.
5. **Recorded date interpretation:** The unusually long recorded lead times should be validated against the organization's actual business definitions and date systems.
6. **External validity:** Results derived from this dataset should not automatically be generalized to other periods, products, factories, or organizations.
7. **Scenario interpretation:** Simulated factory changes are not equivalent to experimentally observed factory changes.

## 7. Recommendations for Future Work

Future research can strengthen the analysis by collecting:

- factory-level capacity and utilization;
- production and processing times;
- transportation distance and freight cost;
- inventory availability and stockouts;
- supplier and manufacturing constraints;
- order priority and service-level requirements;
- historical cases where the same product was manufactured at multiple factories;
- actual operational timestamps rather than only order and ship dates.

With sufficient within-product factory variation, future work could use panel models, fixed effects, causal inference methods, or controlled experiments to estimate factory effects more credibly.

A richer optimization model could then incorporate capacity, cost, distance, service levels, and production constraints. The resulting formulation could be expressed as a constrained assignment or network optimization problem rather than relying only on predictive scenario estimates.

## 8. Conclusion

This study presents a reproducible data-analysis and decision-support framework for investigating shipping lead time and factory-allocation scenarios in a Nassau Candy Distributor dataset. The workflow combines data auditing, exploratory analysis, feature engineering, regression benchmarking, clustering, scenario simulation, and interactive visualization.

Gradient Boosting achieved the strongest benchmark performance among the three evaluated regression models, with a test MAE of 162.586 days, RMSE of 177.767 days, and R² of 0.040. The relatively low explanatory power and the structural confounding between product and factory assignment limit the strength of operational conclusions that can be drawn from the current dataset.

The central contribution of the project is therefore not a definitive factory-reallocation recommendation, but a transparent analytical framework that separates historical evidence from model-based scenarios and explicitly communicates uncertainty. This makes the resulting Streamlit application suitable as an exploratory decision-support tool while identifying the additional data required for stronger operational and causal analysis.

## References

1. Breiman, L. (2001). Random Forests. *Machine Learning, 45*, 5–32.
2. Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine. *The Annals of Statistics, 29*(5), 1189–1232.
3. Rousseeuw, P. J. (1987). Silhouettes: A Graphical Aid to the Interpretation and Validation of Cluster Analysis. *Journal of Computational and Applied Mathematics, 20*, 53–65.
4. Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.
5. McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proceedings of the 9th Python in Science Conference*.

## Reproducibility

The project is organized into separate public repositories for analysis and application deployment. The analysis repository contains notebooks covering auditing, cleaning, EDA, feature engineering, predictive modeling, clustering, scenario simulation, and optimization. The Streamlit repository provides the interactive interface and reusable services.

The repositories intentionally exclude the raw project CSV from version control. The public implementation therefore documents the analytical workflow without redistributing the source dataset.
