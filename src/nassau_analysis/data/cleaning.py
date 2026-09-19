from __future__ import annotations
import pandas as pd
import numpy as np

DATE_FORMAT = "%d-%m-%Y"

def load_raw_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path, dtype={"Postal Code": "string"})

def clean_dataset(df: pd.DataFrame, mapping_path: str) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip() for c in out.columns]
    for col in ["Ship Mode", "Country/Region", "City", "State/Province", "Division", "Region", "Product ID", "Product Name"]:
        out[col] = out[col].astype("string").str.strip()
    out["Order Date"] = pd.to_datetime(out["Order Date"], format=DATE_FORMAT, errors="coerce")
    out["Ship Date"] = pd.to_datetime(out["Ship Date"], format=DATE_FORMAT, errors="coerce")
    out["recorded_lead_time_days"] = (out["Ship Date"] - out["Order Date"]).dt.days
    out["gross_margin_pct"] = np.where(out["Sales"] != 0, out["Gross Profit"] / out["Sales"], np.nan)
    mapping = pd.read_csv(mapping_path)
    mapping["product_name"] = mapping["product_name"].str.strip()
    out = out.merge(mapping[["product_name", "factory"]], left_on="Product Name", right_on="product_name", how="left", validate="many_to_one")
    return out.drop(columns=["product_name"])

def audit_dataset(df: pd.DataFrame) -> dict:
    gross_profit_error = (df["Gross Profit"] - (df["Sales"] - df["Cost"])).abs()
    return {
        "rows": int(len(df)),
        "columns": int(df.shape[1]),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "unique_row_ids": int(df["Row ID"].nunique()),
        "unique_order_ids": int(df["Order ID"].nunique()),
        "unique_products": int(df["Product Name"].nunique()),
        "lead_time_min": int(df["recorded_lead_time_days"].min()),
        "lead_time_median": float(df["recorded_lead_time_days"].median()),
        "lead_time_max": int(df["recorded_lead_time_days"].max()),
        "order_date_min": str(df["Order Date"].min().date()),
        "order_date_max": str(df["Order Date"].max().date()),
        "ship_date_min": str(df["Ship Date"].min().date()),
        "ship_date_max": str(df["Ship Date"].max().date()),
        "gross_profit_consistency_max_abs_error": float(gross_profit_error.max()),
        "mapping_unmatched_products": int(df["factory"].isna().sum()),
    }
