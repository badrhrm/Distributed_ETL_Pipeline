
import pandas as pd
import pyodbc
import os

def extract_database():
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

    query = "SELECT * FROM users"  
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






if __name__ == "__main__":
    print("Running extraction logic...")
    # Test SQL extraction
    print("Testing SQL extraction...")
    extract_database()



