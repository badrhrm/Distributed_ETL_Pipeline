
import pandas as pd
import pyodbc
import os

def extract_database(table_name):
    server = 'localhost'       
    database = 'SysDist'
    username = 'adia'
    password = 'adia'
    driver = '{ODBC Driver 17 for SQL Server}'  
    
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    try:
        conn = pyodbc.connect(connection_string)
        print("Connected to database")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

    query = f"SELECT * FROM {table_name}"  
    print(f"Executing query: {query}")

    try:
        df = pd.read_sql(query, conn)
        if df.empty:
            print("No data found.")
        else:
            print(f"Data extracted:\n{df}")
    except Exception as e:
        print(f"Error during SQL execution: {e}")
    
    conn.close()
    return df


def extract_csv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "physical_shop_sales.csv")
    
    print(f"CSV file path: {csv_path}")  

    if not os.path.exists(csv_path):
        print(f"CSV file not found at: {csv_path}")  
        return None
    
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            print("No csv data found.")
        else:
            print(f"CSV data extracted:\n{df}")
    except Exception as e:
        print(f"Error during CSV extraction: {e}")

    return df

"""

if __name__ == "__main__":
    print("Running extraction logic...")
    # Test SQL extraction
    print("Testing SQL extraction...")
    extract_database()

    # Test CSV extraction
    print("Testing CSV extraction...")
    extract_csv()

"""