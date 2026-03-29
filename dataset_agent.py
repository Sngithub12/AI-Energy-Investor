import pandas as pd

df = pd.read_csv("data/owid-energy-data.csv")

def get_top_solar_countries(top_n=5):
    latest_year = df["year"].max()

    filtered = df[df["year"] == latest_year]

    result = filtered[["country", "solar_share_elec", "renewables_share_elec"]].dropna()

    result = result.sort_values(by="solar_share_elec", ascending=False).head(top_n)

    return result.to_dict(orient="records")