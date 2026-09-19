# Model Evaluation

The models predict `recorded_lead_time_days` using a chronological 80/20 split.

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Gradient Boosting | 162.59 | 177.77 | 0.040 |
| Linear Regression | 180.41 | 182.13 | -0.007 |
| Random Forest | 163.47 | 183.86 | -0.026 |

Gradient Boosting has the lowest RMSE among tested models, but R² is only about 0.04. Predictive explanatory power is therefore weak.
