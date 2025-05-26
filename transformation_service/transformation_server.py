import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_interfaces', 'generated')))

import transformation_pb2
import transformation_pb2_grpc
import common_pb2

import pandas as pd
import io
import transformation_logic # Your first script


from concurrent import futures
import grpc

class TransformationServiceServicer(transformation_pb2_grpc.TransformationServiceServicer):

    def TransformAll(self, request, context):
        # Decode incoming data into a dictionary of DataFrames
        # This 'extracted_data' is effectively the 'data_dictionary'
        # that 'load_and_clean_data' expects.
        extracted_data = {}
        for table in request.tables:
            # Make sure table.table_name matches the keys expected by load_and_clean_data
            # e.g., 'books', 'authors', 'orders', 'order_items', 'users', 'physical_shop_sales'
            df = pd.read_json(io.BytesIO(table.data), orient='records')
            extracted_data[table.table_name] = df

        # 1. Use load_and_clean_data to get the specific DataFrames
        print("--- calling load_and_clean_data from trans server ---")
        # 'extracted_data' here serves as the 'data_dictionary' argument
        online_df, physical_df = transformation_logic.load_and_clean_data(extracted_data)

        # 2. Now call transform_all_data with the two required DataFrames
        print("--- calling transform_all_data from trans server ---")
        transformed_data_dictionary = transformation_logic.transform_all_data(online_df, physical_df)

        # Build response (send back transformed data as bytes)
        # 'transformed_data_dictionary' is the dictionary of DataFrames returned by transform_all_data
        response = transformation_pb2.MultiTransformResponse()
        for table_name, df_to_send in transformed_data_dictionary.items(): # Use the new variable name
            data_bytes = df_to_send.to_json(orient='records').encode('utf-8')
            response.tables.append(
                common_pb2.TableData(table_name=table_name, data=data_bytes)
            )

        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transformation_pb2_grpc.add_TransformationServiceServicer_to_server(TransformationServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    print("Transformation gRPC Server started at port 50052...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()