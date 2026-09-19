from __future__ import annotations
import json
import joblib
import pandas as pd
from importlib.resources import files

def load_model(path: str):
    return joblib.load(path)

def load_selected_model():
    return joblib.load(files("nassau_analysis.artifacts").joinpath("gradient_boosting.joblib"))

def load_model_metrics() -> pd.DataFrame:
    with files("nassau_analysis.artifacts").joinpath("model_metrics.csv").open("r", encoding="utf-8") as f:
        return pd.read_csv(f)

def load_metadata() -> dict:
    with files("nassau_analysis.artifacts").joinpath("metadata.json").open("r", encoding="utf-8") as f:
        return json.load(f)

def predict(model, rows: pd.DataFrame):
    return model.predict(rows)
