import pickle
import numpy as np
import pandas as pd
import streamlit as st

# Load trained KMeans model and dataset
with open("ML_models/Tournments_dataset/Tournment Stability Score/stability_cluster.pkl", "rb") as f:
    kmeans, df_grouped = pickle.load(f)

# Function to explain cluster
def explain_cluster(cluster: int):
    if cluster == 0:
        return "🔴 Cluster 0: Low prize pool, high instability → ❌ Risky investment"
    elif cluster == 1:
        return "🟡 Cluster 1: Medium prize pool, stable → ⚖️ Good long-term bet"
    elif cluster == 2:
        return "🟢 Cluster 2: High prize pool, very stable → ✅ Premium investment"
    else:
        return "Unknown cluster"

# Streamlit App
st.title("🏆 Tournament Stability Score")
st.write("Analyze tournament prize pools and stability using **KMeans clustering**")

# Option for input
option = st.radio("Select Input Mode:", ["Search Tournament from DB", "Enter Prize Pools Manually"])

if option == "Search Tournament from DB":
    tournament_list = df_grouped["tournament_name"].unique().tolist()
    tname = st.selectbox("Select a tournament:", tournament_list)

    if st.button("Predict Cluster"):
        row = df_grouped[df_grouped["tournament_name"].str.lower() == tname.lower()]
        if not row.empty:
            cluster = int(row.iloc[0]["cluster"])
            st.success(f"Tournament **{tname}** belongs to **Cluster {cluster}**")
            st.info(explain_cluster(cluster))
        else:
            st.error("Tournament not found in database.")

elif option == "Enter Prize Pools Manually":
    prize_input = st.text_input("Enter past prize pools (comma separated, e.g. 1000000,1200000,1100000):")

    if st.button("Predict from Pools"):
        try:
            prize_pools = [float(x) for x in prize_input.split(",") if x.strip() != ""]
            if len(prize_pools) < 2:
                st.warning("⚠️ Need at least 2 years of prize pool data.")
            else:
                mean_prize = np.mean(prize_pools)
                std_prize = np.std(prize_pools, ddof=0)
                stability = std_prize / mean_prize if mean_prize != 0 else 0

                cluster = int(kmeans.predict([[mean_prize, stability]])[0])

                st.write(f"📊 **Mean Prize:** {mean_prize:.2f}")
                st.write(f"📉 **Stability Score:** {stability:.3f}")
                st.success(f"Tournament belongs to **Cluster {cluster}**")
                st.info(explain_cluster(cluster))
        except ValueError:
            st.error("❌ Invalid input. Please enter numbers only.")

def app():
    st.title("🏆 Tournament Stability Score Predictor")