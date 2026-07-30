import pandas as pd
from pathlib import Path

data_folder = Path("data/raw")

csv_files = list(data_folder.glob("*.csv"))

print("Number of CSV files found:", len(csv_files))

for file in csv_files:
    print("\n" + "=" * 60)
    print("FILE:", file.name)
    print("=" * 60)

    df = pd.read_csv(file)

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())