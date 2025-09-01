from googleapiclient.discovery import build
import pandas as pd
import isodate
import pycountry
from datetime import datetime

API_KEY = "AIzaSyCbzJxbnkP66k1-uYB2fd3Ly_mQOigH2m4"
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_country_name(country_code):
    try:
        return pycountry.countries.get(alpha_2=country_code).name
    except:
        return "Not specified"

def get_channel_details(channel_name):
    search_response = youtube.search().list(
        part="snippet",
        q=channel_name,
        type="channel",
        maxResults=1
    ).execute()

    if not search_response["items"]:
        print(f"Channel not found: {channel_name}")
        return None, None

    channel_id = search_response["items"][0]["snippet"]["channelId"]

    channel_response = youtube.channels().list(
        part="snippet,statistics,contentDetails,status,brandingSettings",
        id=channel_id
    ).execute()

    channel = channel_response["items"][0]
    country_name = get_country_name(channel["snippet"].get("country", ""))
    published_at = datetime.strptime(channel["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    channel_age_years = round((datetime.now() - published_at).days / 365, 2)
    verified_status = channel["status"].get("isVerified", False)

    details = {
        "Channel_Name": channel["snippet"]["title"],
        "Country": country_name,
        "Subscribers": int(channel["statistics"].get("subscriberCount", 0)),
        "Total_Views": int(channel["statistics"].get("viewCount", 0)),
        "Video_Count": int(channel["statistics"].get("videoCount", 0)),
        "Channel_Age_Years": channel_age_years,
        "Verified": verified_status,
        "Language": channel["brandingSettings"]["channel"].get("defaultLanguage", "Not specified"),
        "Published_At": published_at.strftime("%Y-%m-%d")
    }
    return channel_id, details

def get_video_data(channel_id, max_results=20):
    uploads_playlist_id = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist_id,
        maxResults=max_results
    ).execute()

    video_data = []
    video_ids = []

    for item in playlist_response["items"]:
        video_id = item["snippet"]["resourceId"]["videoId"]
        video_ids.append(video_id)
        video_data.append({
            "Title": item["snippet"]["title"],
            "Published_Date": item["snippet"]["publishedAt"]
        })

    video_stats_response = youtube.videos().list(
        part="statistics,contentDetails,snippet",
        id=",".join(video_ids)
    ).execute()

    for i, item in enumerate(video_stats_response["items"]):
        stats = item["statistics"]
        content = item["contentDetails"]

        video_data[i].update({
            "Duration_Minutes": isodate.parse_duration(content["duration"]).total_seconds() / 60,
            "View_Count": int(stats.get("viewCount", 0)),
            "Like_Count": int(stats.get("likeCount", 0)),
            "Comment_Count": int(stats.get("commentCount", 0)),
        })
    return video_data

def calculate_metrics(video_data, channel_info):
    if not video_data:
        return channel_info

    avg_views = sum(v["View_Count"] for v in video_data) / len(video_data)
    avg_likes = sum(v["Like_Count"] for v in video_data) / len(video_data)
    avg_comments = sum(v["Comment_Count"] for v in video_data) / len(video_data)
    avg_duration = sum(v["Duration_Minutes"] for v in video_data) / len(video_data)
    engagement_rate = ((avg_likes + avg_comments) / avg_views) * 100 if avg_views else 0

    highest_video = max(video_data, key=lambda x: x["View_Count"])
    upload_freq = len(video_data) / ((datetime.now() - datetime.strptime(video_data[-1]["Published_Date"], "%Y-%m-%dT%H:%M:%SZ")).days / 7)

    channel_info.update({
        "Avg_Views_Per_Video": round(avg_views, 2),
        "Upload_Freq_Per_Week": round(upload_freq, 2),
        "Avg_Video_Length_Minutes": round(avg_duration, 2),
        "Likes_Per_Video_Avg": round(avg_likes, 2),
        "Comments_Per_Video_Avg": round(avg_comments, 2),
        "Engagement_Rate_Percent": round(engagement_rate, 2),
        "Highest_Views": highest_video["View_Count"],
        "Last_Upload_Date": video_data[0]["Published_Date"]
    })
    return channel_info

def get_full_channel_info(channel_name):
    channel_id, details = get_channel_details(channel_name)
    if not channel_id:
        return None
    video_info = get_video_data(channel_id)
    return calculate_metrics(video_info, details)

# Read channel names from CSV
channels_df = pd.read_csv("channels.csv")  

for ch in channels_df["Channel_Name"]:
    try:
        print(f"Fetching data for {ch}...")
        info = get_full_channel_info(ch)
        if info:
            all_data.append(info)
    except Exception as e:
        print(f" Error fetching {ch}: {e}")

# Save all results in CSV
df = pd.DataFrame(all_data)
df.to_csv("youtube_channels_data.csv", index=False)
print(" Data saved to TopYoutubers.csv")
print(df.head())
