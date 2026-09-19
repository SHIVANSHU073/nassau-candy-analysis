from __future__ import annotations
import pandas as pd

def rank_recommendations(scenarios: pd.DataFrame, speed_weight=0.5, profit_weight=0.25, risk_weight=0.25):
    x = scenarios.copy()
    x["lead_time_improvement_days"] = -x["delta_days"]
    for c in ["lead_time_improvement_days", "profit_exposure", "risk_reduction"]:
        lo, hi = x[c].min(), x[c].max()
        x[c + "_norm"] = 0.0 if hi == lo else (x[c]-lo)/(hi-lo)
    x["recommendation_score"] = speed_weight*x["lead_time_improvement_days_norm"] + profit_weight*x["profit_exposure_norm"] + risk_weight*x["risk_reduction_norm"]
    return x.sort_values("recommendation_score", ascending=False)
