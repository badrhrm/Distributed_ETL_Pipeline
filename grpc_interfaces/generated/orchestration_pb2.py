# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: orchestration.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'orchestration.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13orchestration.proto\x12\rorchestration\x1a\x0c\x63ommon.proto\"J\n\x15UpdateScheduleRequest\x12\x13\n\x0b\x64\x61y_of_week\x18\x01 \x01(\t\x12\x0c\n\x04hour\x18\x02 \x01(\x05\x12\x0e\n\x06minute\x18\x03 \x01(\x05\x32\xa2\x01\n\x14OrchestrationService\x12<\n\x0eOrchestrateETL\x12\x14.common.EmptyRequest\x1a\x14.common.LoadResponse\x12L\n\x0eUpdateSchedule\x12$.orchestration.UpdateScheduleRequest\x1a\x14.common.LoadResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'orchestration_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_UPDATESCHEDULEREQUEST']._serialized_start=52
  _globals['_UPDATESCHEDULEREQUEST']._serialized_end=126
  _globals['_ORCHESTRATIONSERVICE']._serialized_start=129
  _globals['_ORCHESTRATIONSERVICE']._serialized_end=291
# @@protoc_insertion_point(module_scope)
