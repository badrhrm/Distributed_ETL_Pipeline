import pandas as pd
from sqlalchemy import create_engine
import os


def extract_table(engine, table_name):
    query = f"SELECT * FROM {table_name}"
    try:
        df = pd.read_sql(query, engine)
        if df.empty:
            print(f"No data found in table: {table_name}")
    except Exception as e:
        print(f"Error during SQL execution for table {table_name}: {e}")
        df = None
    return df


def extract_csv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "physical_shop_sales.csv")

    if not os.path.exists(csv_path):
        print(f"CSV file not found at: {csv_path}")
        return None

    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            print("CSV file is empty.")
    except Exception as e:
        print(f"Error during CSV extraction: {e}")
        df = None

    return df


def extract_all_data():
    # Direct DB connection parameters
    server = r'DESKTOP-RS85SUQ\SQLEXPRESS'
    database = 'sysdis'
    username = 'sa'
    password = '12345678'

    # SQLAlchemy connection string
    connection_string = (
        f"mssql+pyodbc://{username}:{password}@{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )

    try:
        engine = create_engine(connection_string)
        print("Connected to database via SQLAlchemy.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return {}

    # Extract data from all SQL tables
    tables = [
        'users',
        'authors',
        'books',
        'orders',
        'order_items'
    ]

    results = {}

    for table in tables:
        df = extract_table(engine, table)
        if df is not None:
            results[table] = df

    # Extract data from CSV
    csv_df = extract_csv()
    if csv_df is not None:
        results["physical_shop_sales"] = csv_df

    return results
