import pandas as pd
import io

def load_all_data(data):
    for table_name, data_bytes in data.items():
        df = pd.read_json(io.BytesIO(data_bytes), orient="records")
        if table_name == "books":
            print(f"\n--- Loaded 'books' table ---\n{df}")
