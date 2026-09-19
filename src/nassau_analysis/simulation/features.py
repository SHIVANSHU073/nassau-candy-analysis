from __future__ import annotations
import pandas as pd
from importlib.resources import files

def load_product_defaults() -> pd.DataFrame:
    with files("nassau_analysis.artifacts").joinpath("product_defaults.csv").open("r", encoding="utf-8") as f:
        return pd.read_csv(f)

def build_scenario_row(product: str, region: str, ship_mode: str, factory: str, order_year: int, order_month: int) -> pd.DataFrame:
    defaults = load_product_defaults()
    r = defaults.loc[defaults["Product Name"] == product].iloc[0]
    return pd.DataFrame([{
        "Product Name": product, "Division": r["division"], "Region": region, "Ship Mode": ship_mode,
        "factory": factory, "Units": r["median_units"], "Sales": r["median_sales"], "Cost": r["median_cost"],
        "Gross Profit": r["median_gross_profit"], "gross_margin_pct": r["median_margin"],
        "order_year": order_year, "order_month": order_month, "order_quarter": (order_month-1)//3+1, "order_dayofweek": 2,
    }])
