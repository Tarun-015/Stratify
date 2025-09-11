import psycopg2
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle

conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="Stratify",
    user="postgres",
    password="2004"
)

query = "SELECT channel_name, avg_views_per_video, likes_per_video_avg, comments_per_video_avg FROM topyoutubers;"
df = pd.read_sql(query, conn)
conn.close()


X = df[["avg_views_per_video", "likes_per_video_avg", "comments_per_video_avg"]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Train KMeans
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["Cluster"] = kmeans.fit_predict(X_scaled)

# Map clusters to High/Medium/Low
cluster_order = df.groupby("Cluster")[["likes_per_video_avg", "comments_per_video_avg"]].mean().sum(axis=1).sort_values()
mapping = {cluster: label for cluster, label in zip(cluster_order.index, ["Low", "Medium", "High"])}
df["EngagementCategory"] = df["Cluster"].map(mapping)


with open("yt_engagement.pkl", "wb") as f:
    pickle.dump((kmeans, scaler, mapping), f)

print("Engagement clustering model saved as yt_engagement.pkl")