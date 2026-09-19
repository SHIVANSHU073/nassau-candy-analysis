from __future__ import annotations
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def cluster_segments(df: pd.DataFrame, max_k: int = 6):
    g = df.groupby(["factory", "Region", "Product Name", "Ship Mode"], dropna=False).agg(
        lead_time_mean=("recorded_lead_time_days", "mean"),
        lead_time_std=("recorded_lead_time_days", "std"),
        rows=("Row ID", "count"),
        units=("Units", "sum"),
        sales=("Sales", "sum"),
        gross_profit=("Gross Profit", "sum"),
    ).reset_index().fillna(0)
    features = ["lead_time_mean", "lead_time_std", "rows", "units", "sales", "gross_profit"]
    X = StandardScaler().fit_transform(g[features])
    scores = []
    upper = min(max_k, len(g)-1)
    for k in range(2, upper + 1):
        labels = KMeans(n_clusters=k, random_state=42, n_init=20).fit_predict(X)
        scores.append((k, silhouette_score(X, labels)))
    best_k = max(scores, key=lambda z: z[1])[0] if scores else 2
    model = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    g["cluster"] = model.fit_predict(X)
    return g, model, pd.DataFrame(scores, columns=["k", "silhouette_score"])
