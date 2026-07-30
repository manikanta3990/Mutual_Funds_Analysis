import os
import requests
import pandas as pd

# Create raw data folder if it doesn't exist
os.makedirs("data/raw", exist_ok=True)

# Scheme Codes
schemes = {
    "125497": "scheme_125497",
    "119551": "scheme_119551",
    "120503": "scheme_120503",
    "118632": "scheme_118632",
    "119092": "scheme_119092",
    "120841": "scheme_120841"
}

for code, filename in schemes.items():

    url = f"https://api.mfapi.in/mf/{code}"

    print(f"\nFetching Scheme {code}...")

    response = requests.get(url)

    if response.status_code == 200:

        json_data = response.json()

        df = pd.DataFrame(json_data["data"])

        csv_path = f"data/raw/{filename}.csv"

        df.to_csv(csv_path, index=False)

        print("Saved:", csv_path)

        print("Fund House :", json_data["meta"]["fund_house"])
        print("Scheme Name:", json_data["meta"]["scheme_name"])
        print("Rows :", df.shape[0])

    else:
        print("Failed:", code)