import grpc
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_interfaces', 'generated')))
import extraction_pb2_grpc
import transformation_pb2
import transformation_pb2_grpc
import loading_pb2
import loading_pb2_grpc
import common_pb2


def orchestrate_etl():
    # Step 1: Connect to extraction service and get data
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = extraction_pb2_grpc.ExtractionServiceStub(channel)
        extract_response = stub.ExtractAll(common_pb2.EmptyRequest())
    
    print("Extraction completed.")

    # Step 2: Connect to transformation service and transform data
    with grpc.insecure_channel('localhost:50052') as channel:
        
        stub = transformation_pb2_grpc.TransformationServiceStub(channel)
        transform_request = transformation_pb2.MultiExtractRequest(tables=extract_response.tables)
        transform_response = stub.TransformAll(transform_request)

    print("Transformation completed.")

    # Step 3: Connect to loading service and load data
    with grpc.insecure_channel('localhost:50053') as channel:
         
        stub = loading_pb2_grpc.LoadingServiceStub(channel)
        load_request = loading_pb2.MultiLoadRequest(tables=transform_response.tables)
        load_response = stub.LoadAll(load_request)

    print("Loading completed.")
    print(f"Loading response: {load_response.message}")