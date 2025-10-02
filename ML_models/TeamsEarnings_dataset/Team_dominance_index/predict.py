import streamlit as st
import pickle

# Load data
with open("ML_models/TeamsEarnings_dataset/Team dominance index/dominance_data.pkl", "rb") as f:
    df_grouped = pickle.load(f)

st.title("🏆 Team Dominance Index Analyzer")

# Dropdown for team selection
teams = df_grouped["winningteam"].unique()
selected_team = st.selectbox("Select a team:", ["-- Select a Team --"] + list(teams))

if selected_team != "-- Select a Team --":
    team_data = df_grouped[df_grouped["winningteam"] == selected_team]

    if not team_data.empty:
        dominance_value = team_data["dominance"].values[0]

        st.write(f"### Team: {selected_team}")
        st.write(f"**Dominance Index:** `{dominance_value:.3f}`")

        # Categorization
        if dominance_value > 0.42:
            st.success("🏅 Category: **High Dominance**")
        elif dominance_value > 0.3:
            st.warning("⚖️ Category: **Medium Dominance**")
        else:
            st.error("🥉 Category: **Low Dominance**")

# Option to re-enter (reset dropdown)
if st.button("🔄 Re-enter / Choose Again"):
    st.experimental_rerun()


def app():
    st.title("🏆 Team Dominance Index Predictor")