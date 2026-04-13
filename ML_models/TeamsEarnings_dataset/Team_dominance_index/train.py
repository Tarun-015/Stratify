import psycopg2
import pandas as pd
import pickle
import os

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="Stratify",
    user="postgres",
    password="2004"
)

query = "SELECT winningteam, mapsplayed, mapswon, winrate FROM teamstournaments;"
df = pd.read_sql(query, conn)
conn.close()

#Calculate Dominance Index
df["dominance"] = (df["mapswon"] / df["mapsplayed"]) * (df["winrate"] / 100)

# Aggregate per team 
df_grouped = df.groupby("winningteam").agg({
    "mapsplayed": "sum",
    "mapswon": "sum",
    "winrate": "mean",
    "dominance": "mean"
}).reset_index()


save_path = "ML_models/Teams_dataset/Dominance_Index"
os.makedirs(save_path, exist_ok=True)

with open(f"{save_path}/dominance_data.pkl", "wb") as f:
    pickle.dump(df_grouped, f)

print("Dominance data processed and saved as dominance_data.pkl")
print(df_grouped.head())
