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

query = "SELECT * FROM top_youtubers;"
df = pd.read_sql(query, conn)
conn.close()

features = df[["avg_views_per_video", "likes_", "CommentRate"]].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["EngagementCluster"] = kmeans.fit_predict(X_scaled)

cluster_order = df.groupby("EngagementCluster")["LikesRate"].mean().sort_values().index
cluster_map = {cluster_order[0]: "Low Engagement",
               cluster_order[1]: "Medium Engagement",
               cluster_order[2]: "High Engagement"}
df["EngagementLabel"] = df["EngagementCluster"].map(cluster_map)

print(df[["name", "EngagementLabel"]].head())


with open("engagement_cluster.pkl", "wb") as f:
    pickle.dump((scaler, kmeans, cluster_map), f)

print("Engagement clustering model saved as engagement_cluster.pkl")