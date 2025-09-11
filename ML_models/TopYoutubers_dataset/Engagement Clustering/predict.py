import psycopg2
import pandas as pd
import pickle
from googleapiclient.discovery import build

with open("ML_models\TopYoutubers_dataset\Engagement Clustering\yt_engagement.pkl", "rb") as f:
    kmeans, scaler, mapping = pickle.load(f)


# YouTube API Setup
API_KEY = "AIzaSyCbzJxbnkP66k1-uYB2fd3Ly_mQOigH2m4"   # <-- replace with your real API key
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_channel_id(channel_name):
    """Get channel ID from search query"""
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
    """Fetch subscribers, views, video count (basic stats)"""
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
    """Fetch likes & comments for recent videos"""
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
        return f"Channel not found: {youtuber_name}"

    data = get_channel_stats(channel_id)
    if not data:
        return f"Could not fetch stats for: {youtuber_name}"

    # Fetch avg likes/comments from recent videos
    avg_likes, avg_comments = get_video_stats(channel_id, max_results=10)

    # Compute features
    avg_views = data["total_views"] / max(1, data["video_count"])
    input_df = pd.DataFrame([[
    avg_views,
    avg_likes,
    avg_comments
    ]], columns=["avg_views_per_video", "likes_per_video_avg", "comments_per_video_avg"])

    
    input_scaled = scaler.transform(input_df)
    cluster = kmeans.predict(input_scaled)[0]
    engagement_category = mapping[cluster]
    

    return {
        "Channel\n": data["channel_title"],
        "Subscribers\n": data["subscribers"],
        "Total Views\n": data["total_views"],
        "Videos\n": data["video_count"],
        "Avg Views/Video\n": round(avg_views, 2),
        "Avg Likes/Video\n": round(avg_likes, 2),
        "Avg Comments/Video\n": round(avg_comments, 2),
        "Engagement": engagement_category
    }


# User Input
if __name__ == "__main__":
    name = input("Enter YouTuber name: ")
    result = predict_engagement(name)
    print(result)