import pandas as pd

df = pd.read_csv("tournments_final.csv")

# remove duplicate row
df_cleaned = df.drop_duplicates()


df_cleaned.to_csv("tournments_final.csv", index=False)

print("Duplicates removed. Clean file saved as cleaned_tournaments_distinct.csv")
