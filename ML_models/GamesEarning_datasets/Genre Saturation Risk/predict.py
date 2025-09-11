import pandas as pd
import pickle
import psycopg2
from sklearn.base import BaseEstimator, TransformerMixin

# Custom Transformer (same as in train)
class GenreDominanceCalculator(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        if "game_count" not in X.columns:
            raise ValueError("'game_count' column missing in input!")
        X["genredominance"] = X["totalearnings"] / X["game_count"]
        return X[["genredominance", "totalearnings", "totaltournaments"]]


conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="Stratify",
    user="postgres",
    password="2004"
)


with open("ml_models/gamesearning_datasets/genre saturation risk/genre_saturation.pkl", "rb") as f:
    pipeline = pickle.load(f)

# Load DB data
query = "select * from gamesearning;"
df = pd.read_sql(query, conn)

genres = df["genre"].dropna().unique()

def predict_genre_saturation(game_name: str):
    game_row = df[df["game"].str.lower() == game_name.lower()]

    if not game_row.empty:
        selected_genre = game_row.iloc[0]["genre"]
        game_count = df[df["genre"] == selected_genre].shape[0]

        X_new = pd.DataFrame([{
            "genre": selected_genre,
            "totalearnings": game_row.iloc[0]["totalearnings"],
            "totaltournaments": game_row.iloc[0]["totaltournaments"],
            "game_count": game_count
        }])

    else:
        print("Game not found in DB.")
        print("Available genres:", ", ".join(genres))
        selected_genre = input("Select a genre from above: ").strip()

        if selected_genre not in genres:
            raise ValueError("Invalid genre selected.")

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

    print(f"🎮 Prediction for '{game_name}' (Genre: {selected_genre}): {label}")
    return label


if __name__ == "__main__":
    game_name = input("Enter a game name: ")
    predict_genre_saturation(game_name)
