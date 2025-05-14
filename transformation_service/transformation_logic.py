import pandas as pd

def transform_all_data(data):
    transformed = {}

    for table_name, df in data.items():
        if df is not None:
            df_copy = df.copy()
            if table_name == 'books':
                df_copy.loc[:, :] = None  # Proper way to set all values to None
                print("Transformed 'books' table: all values set to None.")
            transformed[table_name] = df_copy
        else:
            transformed[table_name] = None

    return transformed
