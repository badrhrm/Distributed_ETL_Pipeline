from concurrent import futures
import grpc
import orchestration_logic

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grpc_interfaces', 'generated')))
import common_pb2
import orchestration_pb2_grpc

import orchestration_pb2
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


scheduler = BackgroundScheduler()

class OrchestrationServiceServicer:
    def __init__(self):
        scheduler.add_job(orchestration_logic.orchestrate_etl, CronTrigger(day_of_week='wed', hour=10, minute=0), id="etl_job")
        scheduler.start()
        print("Scheduler started.")

    def OrchestrateETL(self, request, context):
        # Trigger the ETL process
        orchestration_logic.orchestrate_etl()
        return common_pb2.LoadResponse(message="ETL process completed successfully.")

    def UpdateSchedule(self, request, context):
        try:
            scheduler.remove_job("etl_job")
            scheduler.add_job(
                orchestration_logic.orchestrate_etl,
                CronTrigger(day_of_week=request.day_of_week, hour=request.hour, minute=request.minute),
                id="etl_job"
            )
            return orchestration_pb2.LoadResponse(message=f"ETL schedule updated to {request.day_of_week} at {request.hour}:{request.minute}")
        except Exception as e:
            return orchestration_pb2.LoadResponse(message=f"Error: {str(e)}")
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add the orchestration service to the server
    orchestration_pb2_grpc.add_OrchestrationServiceServicer_to_server(OrchestrationServiceServicer(), server)
    server.add_insecure_port('[::]:50054')  # Listening on port 50054
    print("Orchestration gRPC Server started at port 50054...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()