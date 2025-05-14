from concurrent import futures
import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_interfaces', 'generated')))
import loading_pb2
import loading_pb2_grpc
import common_pb2

import loading_logic

class LoadingServiceServicer(loading_pb2_grpc.LoadingServiceServicer):
    def LoadAll(self, request, context):
        # Convert TableData to dict of {table_name: bytes}
        incoming_data = {table.table_name: table.data for table in request.tables}
        loading_logic.load_all_data(incoming_data)
        return common_pb2.LoadResponse(message="Data loaded successfully.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    loading_pb2_grpc.add_LoadingServiceServicer_to_server(LoadingServiceServicer(), server)
    server.add_insecure_port('[::]:50053')
    print("Loading gRPC Server started at port 50053...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
