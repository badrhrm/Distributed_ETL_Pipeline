# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import common_pb2 as common__pb2
import orchestration_pb2 as orchestration__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in orchestration_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class OrchestrationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.OrchestrateETL = channel.unary_unary(
                '/orchestration.OrchestrationService/OrchestrateETL',
                request_serializer=common__pb2.EmptyRequest.SerializeToString,
                response_deserializer=common__pb2.LoadResponse.FromString,
                _registered_method=True)
        self.UpdateSchedule = channel.unary_unary(
                '/orchestration.OrchestrationService/UpdateSchedule',
                request_serializer=orchestration__pb2.UpdateScheduleRequest.SerializeToString,
                response_deserializer=common__pb2.LoadResponse.FromString,
                _registered_method=True)


class OrchestrationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def OrchestrateETL(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateSchedule(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrchestrationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'OrchestrateETL': grpc.unary_unary_rpc_method_handler(
                    servicer.OrchestrateETL,
                    request_deserializer=common__pb2.EmptyRequest.FromString,
                    response_serializer=common__pb2.LoadResponse.SerializeToString,
            ),
            'UpdateSchedule': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateSchedule,
                    request_deserializer=orchestration__pb2.UpdateScheduleRequest.FromString,
                    response_serializer=common__pb2.LoadResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'orchestration.OrchestrationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('orchestration.OrchestrationService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class OrchestrationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def OrchestrateETL(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/orchestration.OrchestrationService/OrchestrateETL',
            common__pb2.EmptyRequest.SerializeToString,
            common__pb2.LoadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateSchedule(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/orchestration.OrchestrationService/UpdateSchedule',
            orchestration__pb2.UpdateScheduleRequest.SerializeToString,
            common__pb2.LoadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
