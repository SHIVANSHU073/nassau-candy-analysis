from __future__ import annotations
from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

CATEGORICAL = ["Product Name", "Division", "Region", "Ship Mode", "factory"]
NUMERIC = ["Units", "Sales", "Cost", "Gross Profit", "gross_margin_pct", "order_year", "order_month", "order_quarter", "order_dayofweek"]

def build_preprocessor():
    return ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), NUMERIC),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL),
    ])

def train_models(data: pd.DataFrame, artifact_dir: str):
    artifact = Path(artifact_dir); artifact.mkdir(parents=True, exist_ok=True)
    from nassau_analysis.features.engineering import make_features
    data = make_features(data).join(data[["Order Date"]]).sort_values("Order Date").reset_index(drop=True)
    split = int(len(data) * 0.8)
    train, test = data.iloc[:split], data.iloc[split:]
    X_train, y_train = train[CATEGORICAL + NUMERIC], train["recorded_lead_time_days"]
    X_test, y_test = test[CATEGORICAL + NUMERIC], test["recorded_lead_time_days"]
    models = {
        "linear_regression": LinearRegression(),
        "random_forest": RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1, min_samples_leaf=3),
        "gradient_boosting": GradientBoostingRegressor(random_state=42, n_estimators=250, learning_rate=0.05, max_depth=3),
    }
    metrics = []
    for name, estimator in models.items():
        pipe = Pipeline([("preprocess", build_preprocessor()), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        metrics.append({"model": name, "MAE": mean_absolute_error(y_test, pred), "RMSE": mean_squared_error(y_test, pred) ** 0.5, "R2": r2_score(y_test, pred)})
        joblib.dump(pipe, artifact / f"{name}.joblib")
    metrics_df = pd.DataFrame(metrics).sort_values(["RMSE", "MAE"]).reset_index(drop=True)
    metrics_df.to_csv(artifact / "model_metrics.csv", index=False)
    metadata = {"target":"recorded_lead_time_days","validation":"chronological 80/20 split","train_rows":len(train),"test_rows":len(test),"warning":"Target is recorded date difference; source dates contain implausibly long shipping intervals. Factory is confounded with product assignment.","selected_model":metrics_df.iloc[0]["model"]}
    (artifact / "metadata.json").write_text(json.dumps(metadata, indent=2))
    return metrics_df, train, test
