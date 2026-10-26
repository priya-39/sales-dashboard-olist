
from pathlib import Path
import pandas as pd

data_folder = Path("data/raw")
csv_files = sorted(data_folder.glob("*.csv"))

print("Total CSV files found:", len(csv_files))

for file in csv_files:
    df = pd.read_csv(file)

    print("\n" + "=" * 55)
    print("File:", file.name)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])
    print("Duplicate rows:", df.duplicated().sum())
    print("Total missing values:", df.isnull().sum().sum())

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    if not missing.empty:
        print("Columns with missing values:")
        print(missing.to_string())
    else:
        print("No missing values.")
