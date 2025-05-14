import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_interfaces', 'generated')))

import transformation_pb2
import transformation_pb2_grpc
import common_pb2

import pandas as pd
import io
import transformation_logic


from concurrent import futures
import grpc

class TransformationServiceServicer(transformation_pb2_grpc.TransformationServiceServicer):

    def TransformAll(self, request, context):
        # Decode incoming data
        extracted_data = {}
        for table in request.tables:
            df = pd.read_json(io.BytesIO(table.data), orient='records')  # Deserialize bytes to DataFrame
            extracted_data[table.table_name] = df

        # Apply transformation logic
        transformed_data = transformation_logic.transform_all_data(extracted_data)

        # Build response (send back transformed data as bytes)
        response = transformation_pb2.MultiTransformResponse()
        for table_name, df in transformed_data.items():
            data_bytes = df.to_json(orient='records').encode('utf-8')
            response.tables.append(
                common_pb2.TableData(table_name=table_name, data=data_bytes)
            )

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transformation_pb2_grpc.add_TransformationServiceServicer_to_server(TransformationServiceServicer(), server)
    server.add_insecure_port('[::]:50052')  # Listening on port 50052
    print("Transformation gRPC Server started at port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()