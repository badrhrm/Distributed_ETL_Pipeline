import grpc
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../grpc_interfaces/generated')))
import orchestration_pb2_grpc
import common_pb2
import orchestration_pb2

def trigger_etl_process():
    try:
        with grpc.insecure_channel('localhost:50054') as channel:   
            stub = orchestration_pb2_grpc.OrchestrationServiceStub(channel)
            request = common_pb2.EmptyRequest()   
            response = stub.OrchestrateETL(request)
        return response.message   
    except Exception as e:
        return f"Error triggering ETL process: {str(e)}"
    

def update_orchestration_schedule(day_of_week, hour, minute):
    with grpc.insecure_channel('localhost:50054') as channel:
        stub = orchestration_pb2_grpc.OrchestrationServiceStub(channel)
        request = orchestration_pb2.UpdateScheduleRequest(
            day_of_week=day_of_week,
            hour=hour,
            minute=minute
        )
        response = stub.UpdateSchedule(request)
        print(f"Schedule updated: {response.message}")