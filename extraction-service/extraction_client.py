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
    
    response = stub.ExtractDatabase(extraction_pb2.EmptyRequest())
    data = json.loads(response.data.decode('utf-8'))
    db_df = pd.DataFrame(data)
    print("Database Data:")
    print(db_df)

    csv_response = stub.ExtractCSV(extraction_pb2.EmptyRequest())
    csv_data = json.loads(csv_response.data.decode('utf-8'))
    csv_df = pd.DataFrame(csv_data)
    print("CSV Data:")
    print(csv_df)

if __name__ == "__main__":
    run()
