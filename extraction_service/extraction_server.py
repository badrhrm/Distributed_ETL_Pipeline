from concurrent import futures
import grpc


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_interfaces', 'generated')))
import extraction_pb2
import extraction_pb2_grpc
import common_pb2

import extraction_logic


class ExtractionServiceServicer(extraction_pb2_grpc.ExtractionServiceServicer):

    def ExtractAll(self, request, context):  
        response = extraction_pb2.MultiExtractResponse()
        all_data = extraction_logic.extract_all_data()

        for table_name, df in all_data.items():
            json_data = df.to_json(orient="records").encode('utf-8')
            response.tables.append(
                common_pb2.TableData(table_name=table_name, data=json_data)
            )

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    extraction_pb2_grpc.add_ExtractionServiceServicer_to_server(ExtractionServiceServicer(), server)   
    server.add_insecure_port('[::]:50051')
    print("Extraction gRPC Server started at port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()