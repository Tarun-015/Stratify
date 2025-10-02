import psycopg2
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

# Custom Transformer
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
query = "select * from gamesearning;"
df = pd.read_sql(query, conn)
conn.close()

# dd game_count per genre
df["game_count"] = df.groupby("genre")["game"].transform("count")

# Target: 1 = over-saturated, 0 = safe
df["label"] = (df["totalearnings"] / df["game_count"] > df["totalearnings"].median()).astype(int)

X = df[["totalearnings", "totaltournaments", "game_count"]]
y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline
pipeline = Pipeline([
    ("genre_dominance", GenreDominanceCalculator()),
    ("clf", LogisticRegression())
])

# Train model
pipeline.fit(X_train, y_train)

# save 
with open("ml_models/gamesearning_datasets/genre saturation risk/genre_saturation.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("Model trained and saved as genre_saturation.pkl")
