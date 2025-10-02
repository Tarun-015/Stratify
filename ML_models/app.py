import streamlit as st

# Import all prediction modules
from GamesEarning_datasets.Genre_Saturation_Risk import predict1
from TeamsEarnings_dataset.Prize_to_Hype_ratio import predict as ph_ratio
from TeamsEarnings_dataset.Team_dominance_index import predict as team_dom
from TopYoutubers_dataset.Engagement_Clustering import predict as yt_engage
from TopYoutubers_dataset.Growth_Efficiency_index import predict as yt_growth
from Tournments_dataset.Tournment_Stability_Score import predict as tourn_stability

st.sidebar.title("Select Prediction Module")
option = st.sidebar.radio(
    "Choose a model:",
    (
        "Genre Saturation Risk",
        "Prize-to-Hype Ratio",
        "Team Dominance Index",
        "YouTube Engagement Clustering",
        "YouTube Growth Efficiency",
        "Tournament Stability Score"
    )
)

if option == "Genre Saturation Risk":
    predict1.app()
elif option == "Prize-to-Hype Ratio":
    ph_ratio.app()
elif option == "Team Dominance Index":
    team_dom.app()
elif option == "YouTube Engagement Clustering":
    yt_engage.app()
elif option == "YouTube Growth Efficiency":
    yt_growth.app()
elif option == "Tournament Stability Score":
    tourn_stability.app()
