from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass
class ScenarioResult:
    current_factory: str
    alternative_factory: str
    predicted_lead_time: float | None
    baseline_predicted_lead_time: float | None
    delta_days: float | None
    confidence_score: float
    evidence_type: str
    warnings: list[str]

def simulate_factory_switch(model, row: pd.Series, current_factory: str, alternative_factory: str) -> ScenarioResult:
    warnings = [
        "No historical within-product factory variation was supplied; alternative-factory effect is not causally identified.",
        "Factory capacity, shipping cost, and production constraints are unavailable.",
        "Lead-time target is based on anomalously long recorded date differences."
    ]
    base = row.to_frame().T.copy(); base["factory"] = current_factory
    alt = base.copy(); alt["factory"] = alternative_factory
    baseline = float(model.predict(base)[0]); alternative = float(model.predict(alt)[0])
    return ScenarioResult(current_factory, alternative_factory, alternative, baseline, alternative-baseline, 0.25, "model-based counterfactual proxy", warnings)
