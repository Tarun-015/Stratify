import streamlit as st
import pandas as pd
import pickle
import psycopg2
from sklearn.base import BaseEstimator, TransformerMixin

# --- Custom Transformer ---
class GenreDominanceCalculator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        if "game_count" not in X.columns:
            raise ValueError("'game_count' column missing in input!")
        X["genredominance"] = X["totalearnings"] / X["game_count"]
        return X[["genredominance", "totalearnings", "totaltournaments"]]

# --- DB Connection ---
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        database="Stratify",
        user="postgres",
        password="2004"
    )

conn = get_connection()

# --- Load Model ---
with open("ml_models/gamesearning_datasets/genre saturation risk/genre_saturation.pkl", "rb") as f:
    pipeline = pickle.load(f)

# --- Load Data ---
@st.cache_data
def load_data():
    query = "SELECT * FROM gamesearning;"
    return pd.read_sql(query, conn)

df = load_data()
genres = df["genre"].dropna().unique()

# --- UI ---
st.title("🎮 Genre Saturation Risk Predictor")
st.write("Check whether a game genre is **Safe** or **Over-Saturated** for investment.")

game_name = st.text_input("Enter a Game Name:")

if st.button("Predict"):
    if not game_name.strip():
        st.warning("Please enter a game name.")
    else:
        game_row = df[df["game"].str.lower() == game_name.lower()]

        # ✅ Case 1: Game found in DB
        if not game_row.empty:
            selected_genre = game_row.iloc[0]["genre"]
            game_count = df[df["genre"] == selected_genre].shape[0]

            X_new = pd.DataFrame([{
                "genre": selected_genre,
                "totalearnings": game_row.iloc[0]["totalearnings"],
                "totaltournaments": game_row.iloc[0]["totaltournaments"],
                "game_count": game_count
            }])

            pred = pipeline.predict(X_new)[0]
            label = "Over-Saturated" if pred == 1 else "Safe"

            if label == "Safe":
                st.success(f"✅ Prediction for **{game_name}** (Genre: {selected_genre}): **{label}**")
            else:
                st.error(f"⚠️ Prediction for **{game_name}** (Genre: {selected_genre}): **{label}**")

        # ✅ Case 2: Game not found
        else:
            st.error("❌ Game not found in DB.")
            selected_genre = st.selectbox("Select a Genre:", genres)

            if selected_genre and st.button("Run Prediction"):
                genre_stats = df[df["genre"] == selected_genre].agg({
                    "totalearnings": "mean",
                    "totaltournaments": "mean"
                })
                game_count = df[df["genre"] == selected_genre].shape[0]

                X_new = pd.DataFrame([{
                    "genre": selected_genre,
                    "totalearnings": genre_stats["totalearnings"],
                    "totaltournaments": genre_stats["totaltournaments"],
                    "game_count": game_count
                }])

                pred = pipeline.predict(X_new)[0]
                label = "Over-Saturated" if pred == 1 else "Safe"

                if label == "Safe":
                    st.success(f"✅ Prediction for **{game_name}** (Genre: {selected_genre}): **{label}**")
                else:
                    st.error(f"⚠️ Prediction for **{game_name}** (Genre: {selected_genre}): **{label}**")

def app():
    st.title("🎮 Genre Saturation Risk Predictor")