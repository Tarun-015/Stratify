import psycopg2
import pandas as pd
import pickle
import os
from sklearn.cluster import KMeans

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="Stratify",
    user="postgres",
    password="2004"
)

query = "SELECT tournament_name, year, prize_pool_usd FROM tournaments;"
df = pd.read_sql(query, conn)
conn.close()


df_grouped = df.groupby("tournament_name")["prize_pool_usd"].agg(["mean", "std"]).reset_index()

# NaN std with 0
df_grouped["std"] = df_grouped["std"].fillna(0)


df_grouped["mean"] = df_grouped["mean"].replace(0, 1e-6)

# stability formula
df_grouped["stability"] = df_grouped["std"] / df_grouped["mean"]


X = df_grouped[["mean", "stability"]]

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_grouped["cluster"] = kmeans.fit_predict(X)

#saving...
save_path = "ML_models/Tournaments_dataset/Tournament_Stability_Score"
os.makedirs(save_path, exist_ok=True)

with open(f"{save_path}/stability_cluster.pkl", "wb") as f:
    pickle.dump((kmeans, df_grouped), f)

print("Model trained and saved as stability_cluster.pkl")
print(df_grouped.head())