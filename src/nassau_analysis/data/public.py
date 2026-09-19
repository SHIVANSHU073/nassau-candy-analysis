from __future__ import annotations
import json
import pandas as pd
from importlib.resources import files

def read_csv(name: str) -> pd.DataFrame:
    with files("nassau_analysis.artifacts").joinpath(name).open("r", encoding="utf-8") as f:
        return pd.read_csv(f)

def read_json(name: str) -> dict:
    with files("nassau_analysis.artifacts").joinpath(name).open("r", encoding="utf-8") as f:
        return json.load(f)
