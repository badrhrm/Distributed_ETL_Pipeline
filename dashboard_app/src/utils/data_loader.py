import os
import pandas as pd

OUTPUT_DIR = "output"

def get_loaded_data():
    data = {}

    if not os.path.exists(OUTPUT_DIR):
        print("⚠️ Output directory not found.")
        return data

    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".csv"):
            table_name = filename.replace(".csv", "")
            file_path = os.path.join(OUTPUT_DIR, filename)
            try:
                df = pd.read_csv(file_path)
                data[table_name] = df
                print(f"✅ Loaded: {table_name} ({df.shape[0]} rows)")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

    return data
