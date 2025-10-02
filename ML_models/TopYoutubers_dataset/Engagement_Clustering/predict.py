import streamlit as st
import pandas as pd
import pickle
from googleapiclient.discovery import build

# Load Model
with open("ML_models/TopYoutubers_dataset/Engagement Clustering/yt_engagement.pkl", "rb") as f:
    kmeans, scaler, mapping = pickle.load(f)

# YouTube API Setup
API_KEY = "AIzaSyCbzJxbnkP66k1-uYB2fd3Ly_mQOigH2m4"  # ⚠️ apna API key daalo
youtube = build("youtube", "v3", developerKey=API_KEY)


# ---------------- Helper Functions ----------------
def get_channel_id(channel_name):
    request = youtube.search().list(
        q=channel_name,
        part="snippet",
        type="channel",
        maxResults=1
    )
    response = request.execute()
    if not response["items"]:
        return None
    return response["items"][0]["snippet"]["channelId"]

def get_channel_stats(channel_id):
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()
    if not response["items"]:
        return None
    item = response["items"][0]
    stats = item["statistics"]
    return {
        "channel_title": item["snippet"]["title"],
        "subscribers": int(stats.get("subscriberCount", 0)),
        "total_views": int(stats.get("viewCount", 0)),
        "video_count": int(stats.get("videoCount", 1))
    }

def get_video_stats(channel_id, max_results=10):
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    )
    response = request.execute()
    uploads_playlist = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist,
        maxResults=max_results
    )
    response = request.execute()
    video_ids = [item["contentDetails"]["videoId"] for item in response["items"]]

    likes, comments = [], []
    for vid in video_ids:
        req = youtube.videos().list(
            part="statistics",
            id=vid
        )
        res = req.execute()
        if res["items"]:
            vstats = res["items"][0]["statistics"]
            likes.append(int(vstats.get("likeCount", 0)))
            comments.append(int(vstats.get("commentCount", 0)))

    avg_likes = sum(likes) / len(likes) if likes else 0
    avg_comments = sum(comments) / len(comments) if comments else 0

    return avg_likes, avg_comments


def predict_engagement(youtuber_name):
    channel_id = get_channel_id(youtuber_name)
    if not channel_id:
        return None, f"❌ Channel not found: {youtuber_name}"

    data = get_channel_stats(channel_id)
    if not data:
        return None, f"❌ Could not fetch stats for: {youtuber_name}"

    # Fetch avg likes/comments from recent videos
    avg_likes, avg_comments = get_video_stats(channel_id, max_results=10)

    # Compute features
    avg_views = data["total_views"] / max(1, data["video_count"])
    input_df = pd.DataFrame([[avg_views, avg_likes, avg_comments]],
                            columns=["avg_views_per_video", "likes_per_video_avg", "comments_per_video_avg"])

    input_scaled = scaler.transform(input_df)
    cluster = kmeans.predict(input_scaled)[0]
    engagement_category = mapping[cluster]

    # Fetch channel start year
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()
    start_year = response["items"][0]["snippet"]["publishedAt"].split("-")[0]

    result = {
        "Channel": data["channel_title"],
        "Subscribers": data["subscribers"],
        "Total Views": data["total_views"],
        "Videos": data["video_count"],
        "Avg Views/Video": round(avg_views, 2),
        "Avg Likes/Video": round(avg_likes, 2),
        "Avg Comments/Video": round(avg_comments, 2),
        "Engagement": engagement_category,
        "Channel Start Year": start_year
    }
    return result, None


# ---------------- Streamlit UI ----------------
st.title("📊 YouTuber Engagement Prediction")
st.write("Enter a YouTube channel name to analyze engagement using clustering model (KMeans).")

youtuber_name = st.text_input("🔍 Enter YouTuber Name:")

if st.button("Predict Engagement"):
    if not youtuber_name.strip():
        st.warning("Please enter a channel name.")
    else:
        with st.spinner("Fetching data... Please wait ⏳"):
            result, error = predict_engagement(youtuber_name)

        if error:
            st.error(error)
        else:
            st.success(f"✅ Engagement Prediction for {result['Channel']}")
            st.json(result)

def app():
    st.title("📊 Engagement Clustering")