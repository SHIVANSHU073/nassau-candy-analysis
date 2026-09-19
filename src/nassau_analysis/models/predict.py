from __future__ import annotations

import json
import warnings
from importlib.resources import files

import joblib
import pandas as pd


class HistoricalScenarioProxy:
    """Dependency-light fallback when the packaged binary model cannot be loaded.

    This is intentionally NOT a factory-effect model. It estimates recorded lead
    time from historical product/region/ship-mode means and therefore gives the
    same baseline across factories. That is preferable to silently presenting
    corrupted-artifact output as a causal factory effect.
    """

    def __init__(self):
        self.product = pd.read_csv(files("nassau_analysis.artifacts").joinpath("product_summary.csv"))
        self.region = pd.read_csv(files("nassau_analysis.artifacts").joinpath("region_summary.csv"))
        self.ship_mode = pd.read_csv(files("nassau_analysis.artifacts").joinpath("ship_mode_summary.csv"))
        self.overall = float(self.product["lead_time_mean"].mul(self.product["rows"]).sum() / self.product["rows"].sum())

    def predict(self, rows: pd.DataFrame):
        out = []
        for _, row in rows.iterrows():
            p = self.product.loc[self.product["Product Name"] == row["Product Name"], "lead_time_mean"]
            r = self.region.loc[self.region["Region"] == row["Region"], "lead_time_mean"]
            s = self.ship_mode.loc[self.ship_mode["Ship Mode"] == row["Ship Mode"], "lead_time_mean"]
            pred = self.overall
            if len(p):
                pred += float(p.iloc[0]) - self.overall
            if len(r):
                pred += float(r.iloc[0]) - self.overall
            if len(s):
                pred += float(s.iloc[0]) - self.overall
            out.append(pred)
        return out


def load_model(path: str):
    return joblib.load(path)


def load_selected_model():
    """Load the packaged model, with a safe deterministic fallback.

    The public application must remain usable even if a binary artifact is
    damaged or incompatible with the deployment environment.
    """
    model_path = files("nassau_analysis.artifacts").joinpath("gradient_boosting.joblib")
    try:
        return joblib.load(model_path)
    except Exception as exc:
        warnings.warn(
            f"Packaged Gradient Boosting artifact could not be loaded; using "
            f"HistoricalScenarioProxy instead: {type(exc).__name__}: {exc}",
            RuntimeWarning,
        )
        return HistoricalScenarioProxy()


def load_model_metrics() -> pd.DataFrame:
    with files("nassau_analysis.artifacts").joinpath("model_metrics.csv").open("r", encoding="utf-8") as f:
        return pd.read_csv(f)


def load_metadata() -> dict:
    with files("nassau_analysis.artifacts").joinpath("metadata.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def predict(model, rows: pd.DataFrame):
    return model.predict(rows)
