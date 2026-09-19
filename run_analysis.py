from pathlib import Path
import sys, json, argparse
import pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).parent/'src'))
from nassau_analysis.data.cleaning import load_raw_csv, clean_dataset, audit_dataset
from nassau_analysis.models.train import train_models
from nassau_analysis.clustering.routes import cluster_segments

ROOT=Path(__file__).parent
parser=argparse.ArgumentParser()
parser.add_argument('--csv', required=True)
args=parser.parse_args()
RAW=Path(args.csv); MAP=ROOT/'reference_data'/'product_factory_mapping.csv'
OUT=ROOT/'outputs'; MODELS=ROOT/'models'/'trained_models'
for p in [OUT/'tables',OUT/'figures',OUT/'recommendations',MODELS]: p.mkdir(parents=True,exist_ok=True)
df=load_raw_csv(RAW); clean=clean_dataset(df,MAP); audit=audit_dataset(clean)
(OUT/'tables'/'data_audit.json').write_text(json.dumps(audit,indent=2))
clean.groupby('Product Name').agg(rows=('Row ID','count'),units=('Units','sum'),sales=('Sales','sum'),gross_profit=('Gross Profit','sum'),lead_time_mean=('recorded_lead_time_days','mean'),lead_time_median=('recorded_lead_time_days','median')).sort_values('sales',ascending=False).to_csv(OUT/'tables'/'product_summary.csv')
clean.groupby('Region').agg(rows=('Row ID','count'),units=('Units','sum'),sales=('Sales','sum'),gross_profit=('Gross Profit','sum'),lead_time_mean=('recorded_lead_time_days','mean'),lead_time_median=('recorded_lead_time_days','median')).sort_values('sales',ascending=False).to_csv(OUT/'tables'/'region_summary.csv')
clean.groupby('Ship Mode').agg(rows=('Row ID','count'),sales=('Sales','sum'),gross_profit=('Gross Profit','sum'),lead_time_mean=('recorded_lead_time_days','mean'),lead_time_median=('recorded_lead_time_days','median')).to_csv(OUT/'tables'/'ship_mode_summary.csv')
clean['lead_time_bucket']=pd.cut(clean['recorded_lead_time_days'],bins=[-1,100,500,1000,1200,1300,1500,1700],labels=['<=100','101-500','501-1000','1001-1200','1201-1300','1301-1500','1501-1700'])
clean.groupby('lead_time_bucket',observed=False).size().rename('rows').to_csv(OUT/'tables'/'lead_time_buckets.csv')
plt.figure(figsize=(8,5)); clean['recorded_lead_time_days'].hist(bins=40); plt.xlabel('Recorded lead time (days)'); plt.ylabel('Rows'); plt.title('Recorded Lead-Time Distribution'); plt.tight_layout(); plt.savefig(OUT/'figures'/'lead_time_distribution.png',dpi=160); plt.close()
plt.figure(figsize=(9,5)); clean.groupby('Region')['recorded_lead_time_days'].median().sort_values().plot(kind='bar'); plt.ylabel('Median recorded lead time (days)'); plt.title('Median Recorded Lead Time by Region'); plt.tight_layout(); plt.savefig(OUT/'figures'/'lead_time_by_region.png',dpi=160); plt.close()
metrics,train,test=train_models(clean,str(MODELS)); metrics.to_csv(OUT/'tables'/'model_comparison.csv',index=False)
clusters,cluster_model,silhouette=cluster_segments(clean); clusters.to_csv(OUT/'tables'/'segment_clusters.csv',index=False); silhouette.to_csv(OUT/'tables'/'cluster_selection.csv',index=False)
seg=clean.groupby(['Product Name','Region','factory']).agg(rows=('Row ID','count'),units=('Units','sum'),sales=('Sales','sum'),gross_profit=('Gross Profit','sum'),lead_time_mean=('recorded_lead_time_days','mean')).reset_index()
seg['gross_margin_pct']=seg['gross_profit']/seg['sales']; seg['priority_exposure']=seg['sales']*seg['lead_time_mean']
seg.sort_values('priority_exposure',ascending=False).head(25).to_csv(OUT/'recommendations'/'priority_segments.csv',index=False)
print(json.dumps(audit,indent=2)); print(metrics.to_string(index=False)); print(silhouette.to_string(index=False))
