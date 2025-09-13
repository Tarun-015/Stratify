import pickle

with open("ML_models/TeamsEarnings_dataset/Team dominance index/dominance_data.pkl", "rb") as f:
    df_grouped = pickle.load(f)

while True:
    team_name = input("Enter a team name: ").strip()

    # Check if team exists
    team_data = df_grouped[df_grouped["winningteam"].str.lower() == team_name.lower()]

    if team_data.empty:
        print(f"Team '{team_name}' not found in database.")
        print("Available teams:", ", ".join(df_grouped["winningteam"].unique()[:10]), "...")
        print("Please try again.\n")
    else:
        dominance_value = team_data["dominance"].values[0]
        print(f"\nTeam: {team_name}")
        print(f"Dominance Index: {dominance_value:.3f}")

        # categorization
        if dominance_value > 0.6:
            print("Category: High Dominance")
        elif dominance_value > 0.3:
            print("Category: Medium Dominance")
        else:
            print("Category: Low Dominance")
        break