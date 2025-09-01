import pickle
import pandas as pd

with open("ML_models\TopYoutubers_dataset\Growth_Efficiency_index\yt_classifier.pkl", "rb") as f:
    model = pickle.load(f)

years_active = int(input("Years Active: "))
views = int(input("Total Views: "))
subs = int(input("Subscribers: "))

growth_eff = subs / years_active if years_active > 0 else 0

user_data = pd.DataFrame({
    "channel_age_years": [years_active],
    "total_views": [views],
    "GrowthEfficiency": [growth_eff]
})

prediction = model.predict(user_data)[0]
print(f"Investment Category: {prediction}")