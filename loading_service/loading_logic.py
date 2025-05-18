import pandas as pd
import io

# Function to load all data from a dictionary of table names and serialized data
def load_all_data(data):
    # Iterate over each table name and its corresponding data bytes
    for table_name, data_bytes in data.items():
        # Convert the byte stream into a pandas DataFrame
        df = pd.read_json(io.BytesIO(data_bytes), orient="records")
        
        # If the current table is 'books', print its content for verification
        if table_name == "books":
            print(f"\n--- Loaded 'books' table ---\n{df}")
