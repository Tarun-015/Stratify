import streamlit as st
import pickle
import pandas as pd

# Load model
with open("ML_models/TopYoutubers_dataset/Growth_Efficiency_index/yt_classifier.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------- UI ----------------
st.title("📈 YouTuber Growth Efficiency Index")
st.write("Predict investment category based on channel's growth and engagement efficiency.")

# User inputs
years_active = st.number_input("⏳ Years Active", min_value=0, step=1)
views = st.number_input("👁️ Total Views", min_value=0, step=1000)
subs = st.number_input("👥 Subscribers", min_value=0, step=1000)

if st.button("Predict Investment Category"):
    if years_active == 0:
        growth_eff = 0
    else:
        growth_eff = subs / years_active

    # Create DataFrame
    user_data = pd.DataFrame({
        "channel_age_years": [years_active],
        "total_views": [views],
        "GrowthEfficiency": [growth_eff]
    })

    # Prediction
    prediction = model.predict(user_data)[0]

    # Display results
    st.success(f"✅ Investment Category: **{prediction}**")

    st.subheader("📊 Features Used")
    st.write(user_data)
<<<<<<< HEAD
=======


def app():
    st.title("📊 YouTuber Growth Efficiency Index")
>>>>>>> f985831
