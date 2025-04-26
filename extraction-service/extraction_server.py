from concurrent import futures
import grpc

import sys
sys.path.append('./generated')
import generated.extraction_pb2 as extraction_pb2
import generated.extraction_pb2_grpc as extraction_pb2_grpc

import extraction_logic
#import json


class ExtractionServiceServicer(extraction_pb2_grpc.ExtractionServiceServicer):
    def ExtractDatabase(self, request, context):
        table_name = request.table_name
        df = extraction_logic.extract_database(table_name)
        json_data = df.to_json(orient="records")
        return extraction_pb2.ExtractResponse(data=json_data.encode('utf-8'))

    def ExtractCSV(self, request, context):
        df = extraction_logic.extract_csv()
        json_data = df.to_json(orient="records")
        return extraction_pb2.ExtractResponse(data=json_data.encode('utf-8'))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    extraction_pb2_grpc.add_ExtractionServiceServicer_to_server(ExtractionServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Extraction gRPC Server started at port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
