import psycopg2
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="Stratify",
    user="postgres",
    password="2004"
)

query = "SELECT * FROM topyoutubers;"
df = pd.read_sql(query, conn)
conn.close()

df["GrowthEfficiency"] = df["subscribers"] / df["channel_age_years"]

def categorize(g):
    if g > 100000:
        return "High Potential"
    elif g >= 10000:
        return "Medium Potential"
    else:
        return "Low Potential"

df["InvestmentCategory"] = df["GrowthEfficiency"].apply(categorize)

X = df[["channel_age_years", "total_views", "GrowthEfficiency"]]
y = df["InvestmentCategory"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

with open("yt_classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("Classification model saved as yt_classifier.pkl")