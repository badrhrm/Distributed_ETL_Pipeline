import pandas as pd
import io

# Dictionary to hold loaded DataFrames for other services (e.g., transformation)
loaded_data = {
    
}

# Main function to load data from incoming byte streams
def load_all_data(data: dict):
    global loaded_data
    print("📦 Loading data...")

    # Convert each byte stream to a pandas DataFrame
    for table_name, data_bytes in data.items():
        try:
            df = pd.read_json(io.BytesIO(data_bytes), orient="records")
            loaded_data[table_name] = df
            print(f"✅ Loaded table: {table_name} - {df.shape[0]} rows")
        except Exception as e:
            print(f"❌ Failed to load {table_name}: {e}")

    # Preview one of the tables (optional)
    if "books" in loaded_data:
        print(f"\n📚 Books Sample:\n{loaded_data['books'].head()}")

# Provide access to loaded data dictionary
def get_loaded_data():
    return loaded_data
