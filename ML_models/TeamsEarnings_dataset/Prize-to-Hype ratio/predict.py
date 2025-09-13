import pickle

with open("ML_models/TeamsEarnings_dataset/Prize-to-Hype ratio/ph_ratio_data.pkl", "rb") as f:
    df_grouped = pickle.load(f)


while True:
    tournament_name = input("Enter a tournament name: ").strip()

    # Check tournament exists
    tournament_data = df_grouped[df_grouped["tournament"].str.lower() == tournament_name.lower()]

    if tournament_data.empty:
        print(f"Tournament '{tournament_name}' not found in database.")
        print("Available tournaments:", ", ".join(df_grouped["tournament"].unique()[:10]), "...")
        print("Please try again.\n")
    else:
        ph_value = tournament_data["ph_ratio"].values[0]
        print(f"\nTournament: {tournament_name}")
        print(f"Prize-to-Hype Ratio: {ph_value:.3f}")

        # categorization
        if ph_value < 1:
            print("Category: Highly Efficient (great hype for less prize money)")
        elif ph_value < 5:
            print("Category: Balanced Efficiency")
        else:
            print("Category: Costly Hype (too much money for too little viewers)")
        break
