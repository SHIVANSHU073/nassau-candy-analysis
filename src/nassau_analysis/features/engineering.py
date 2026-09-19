from __future__ import annotations
import pandas as pd

TARGET = "recorded_lead_time_days"
FEATURE_COLUMNS = [
    "Product Name", "Division", "Region", "Ship Mode", "factory",
    "Units", "Sales", "Cost", "Gross Profit", "gross_margin_pct",
    "order_year", "order_month", "order_quarter", "order_dayofweek",
]

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df.copy()
    x["order_year"] = x["Order Date"].dt.year
    x["order_month"] = x["Order Date"].dt.month
    x["order_quarter"] = x["Order Date"].dt.quarter
    x["order_dayofweek"] = x["Order Date"].dt.dayofweek
    return x[FEATURE_COLUMNS + [TARGET]]
