import pandas as pd

# Load original file
df = pd.read_csv("tournments_final.csv")

# Group by Tournament + Year and aggregate
grouped = df.groupby(["Tournament Name", "Year"], as_index=False).agg({
    "Game": "first",
    "Genre": "first",
    "Organizer": "first",
    "Frequency": "first",
    "Country": "first",
    "Prize Pool (USD)": "max",
    "Prize Pool (USD)_Adjusted": "max"
})

# Save to new file
output_file = "tournaments_grouped.csv"
grouped.to_csv(output_file, index=False)

print(f"File saved as {output_file}")
