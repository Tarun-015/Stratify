import pickle
import numpy as np
import pandas as pd


with open("ML_models\Tournments_dataset\Tournment Stability Score\stability_cluster.pkl", "rb") as f:
    kmeans, df_grouped = pickle.load(f)

def predict_tournament_cluster(tournament_name: str):
    # Search in trained dataset
    row = df_grouped[df_grouped["tournament_name"].str.lower() == tournament_name.lower()]

    if not row.empty:
        cluster = int(row.iloc[0]["cluster"])
        print(f"\nTournament '{tournament_name}' belongs to Cluster {cluster}")
        explain_cluster(cluster)
    else:
        print(f"\nTournament '{tournament_name}' not found in DB.")
        pools_input = input("Enter past prize pools (comma separated, e.g. 1000000,1200000,1100000): ").strip()
        try:
            prize_pools = [float(x) for x in pools_input.split(",") if x.strip() != ""]
            if len(prize_pools) < 2:
                print("Need at least 2 years of prize pool data to calculate stability.")
                return
        except ValueError:
            print("Invalid input. Please enter numeric values separated by commas.")
            return

        mean_prize = np.mean(prize_pools)
        std_prize = np.std(prize_pools, ddof=0)  # population std
        stability = std_prize / mean_prize if mean_prize != 0 else 0

        cluster = int(kmeans.predict([[mean_prize, stability]])[0])
        print(f"\nCalculated mean prize: {mean_prize:.2f}, stability: {stability:.3f}")
        print(f"Based on your input, tournament belongs to Cluster {cluster}")
        explain_cluster(cluster)

def explain_cluster(cluster: int):
    if cluster == 0:
        print("Cluster 0: Low prize pool, high instability → Risky investment")
    elif cluster == 1:
        print("Cluster 1: Medium prize pool, stable → Good long-term bet")
    elif cluster == 2:
        print("Cluster 2: High prize pool, very stable → Premium investment")
    else:
        print("Unknown cluster")

if __name__ == "__main__":
    tname = input("Enter tournament name: ")
    predict_tournament_cluster(tname)