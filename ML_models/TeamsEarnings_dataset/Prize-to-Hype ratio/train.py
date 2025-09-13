# train.py
import psycopg2
import pandas as pd
import pickle
import os

# ---- DB Connection ----
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="Stratify",
    user="postgres",
    password="2004"
)

# ---- Load data ----
query = "SELECT tournament, prizepoolusd, peakviewers FROM teamstournaments;"
df = pd.read_sql(query, conn)
conn.close()

# ---- Calculate Prize-to-Hype Ratio ----
df["ph_ratio"] = df["prizepoolusd"] / df["peakviewers"]

# ---- Aggregate per tournament ----
df_grouped = df.groupby("tournament").agg({
    "prizepoolusd": "sum",
    "peakviewers": "sum",
    "ph_ratio": "mean"
}).reset_index()

# ---- Save processed data for prediction ----
save_path = "ML_models/Tournaments_dataset/Prize_to_Hype_Ratio"
os.makedirs(save_path, exist_ok=True)

with open(f"{save_path}/ph_ratio_data.pkl", "wb") as f:
    pickle.dump(df_grouped, f)

print("✅ P/H Ratio data processed and saved as ph_ratio_data.pkl")
print(df_grouped.head())
