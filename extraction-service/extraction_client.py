import grpc

import sys
sys.path.append('./generated')
import generated.extraction_pb2 as extraction_pb2
import generated.extraction_pb2_grpc as extraction_pb2_grpc
import pandas as pd
import json

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = extraction_pb2_grpc.ExtractionServiceStub(channel)

    tables_to_extract = [
    'users',
    'categories',
    'authors',
    'books',
    'book_categories',
    'book_authors',
    'orders',
    'order_items'
]

    for table in tables_to_extract:
        print(f"Extracting from table: {table}")
        request = extraction_pb2.DatabaseRequest(table_name=table)
        db_response = stub.ExtractDatabase(request)
        db_data = json.loads(db_response.data.decode('utf-8'))
        db_df = pd.DataFrame(db_data)
        print(db_df)
        print("\n" + "="*50 + "\n")
    

    csv_response = stub.ExtractCSV(extraction_pb2.EmptyRequest())
    csv_data = json.loads(csv_response.data.decode('utf-8'))
    csv_df = pd.DataFrame(csv_data)
    print("CSV Data:")
    print(csv_df)

if __name__ == "__main__":
    run()
