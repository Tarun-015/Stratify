import streamlit as st
import pickle
import pandas as pd

# --- Load Data ---
with open("ML_models/TeamsEarnings_dataset/Prize-to-Hype ratio/ph_ratio_data.pkl", "rb") as f:
    df_grouped = pickle.load(f)

# --- Streamlit UI ---
st.title("🏆 Prize-to-Hype Ratio Analyzer")
st.write("Check whether a tournament is **Efficient** or **Costly** based on its Prize-to-Hype Ratio.")

# Dropdown for tournament selection
tournaments = df_grouped["tournament"].unique()
selected_tournament = st.selectbox("Select a Tournament:", ["-- Select --"] + list(tournaments))

# Show prediction when a valid tournament is chosen
if selected_tournament != "-- Select --":
    if st.button("Analyze"):
        tournament_data = df_grouped[df_grouped["tournament"] == selected_tournament]

        if not tournament_data.empty:
            ph_value = tournament_data["ph_ratio"].values[0]

            st.subheader(f"Tournament: {selected_tournament}")
            st.write(f"📊 **Prize-to-Hype Ratio**: `{ph_value:.3f}`")

            # Categorization
            if ph_value < 1:
                st.success("✅ Category: **Highly Efficient** (great hype for less prize money)")
            elif ph_value < 5:
                st.info("⚖️ Category: **Balanced Efficiency**")
            else:
                st.error("💸 Category: **Costly Hype** (too much money for too little viewers)")

            # Re-enter option
            if st.button("🔄 Re-analyze another tournament"):
                st.experimental_rerun()

def app():
    st.title("🏆 Prize-to-Hype Ratio Prediction")