import pandas as pd
import io
import os

# Load all data from byte streams, return a dictionary of DataFrames and save them to output/
def load_all_data(data: dict, output_dir="output") -> dict:
    os.makedirs(output_dir, exist_ok=True)
    loaded_data = {}

    print("📦 Loading data and saving to output/")

    for table_name, data_bytes in data.items():
        try:
            df = pd.read_json(io.BytesIO(data_bytes), orient="records")
            loaded_data[table_name] = df

            # Print summary info
            print(f"✅ {table_name}: {df.shape[0]} rows, {df.shape[1]} columns")

            # Save to CSV
            df.to_csv(os.path.join(output_dir, f"{table_name}.csv"), index=False)

        except Exception as e:
            print(f"❌ Failed to load {table_name}: {e}")

    return loaded_data
