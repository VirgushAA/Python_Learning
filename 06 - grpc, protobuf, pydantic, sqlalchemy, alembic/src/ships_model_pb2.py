# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: ships_model.proto
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
    'ships_model.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11ships_model.proto\x12\tspaceship\",\n\x11\x43oordinateRequest\x12\n\n\x02ra\x18\x01 \x01(\x01\x12\x0b\n\x03\x64\x65\x63\x18\x02 \x01(\x01\">\n\x07Officer\x12\x12\n\nfirst_name\x18\x01 \x01(\t\x12\x11\n\tlast_name\x18\x02 \x01(\t\x12\x0c\n\x04rank\x18\x03 \x01(\t\"\xc4\x01\n\tSpaceship\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\'\n\talignment\x18\x02 \x01(\x0e\x32\x14.spaceship.Alignment\x12(\n\nship_class\x18\x03 \x01(\x0e\x32\x14.spaceship.ShipClass\x12\x0e\n\x06length\x18\x04 \x01(\x05\x12\x11\n\tcrew_size\x18\x05 \x01(\x05\x12\r\n\x05\x61rmed\x18\x06 \x01(\x08\x12$\n\x08officers\x18\x07 \x03(\x0b\x32\x12.spaceship.Officer*`\n\tShipClass\x12\x0c\n\x08\x43ORVETTE\x10\x00\x12\x0b\n\x07\x46RIGATE\x10\x01\x12\x0b\n\x07\x43RUISER\x10\x02\x12\r\n\tDESTROYER\x10\x03\x12\x0b\n\x07\x43\x41RRIER\x10\x04\x12\x0f\n\x0b\x44READNOUGHT\x10\x05* \n\tAlignment\x12\x08\n\x04\x41LLY\x10\x00\x12\t\n\x05\x45NEMY\x10\x01\x32T\n\x10SpaceshipService\x12@\n\x08GetShips\x12\x1c.spaceship.CoordinateRequest\x1a\x14.spaceship.Spaceship0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ships_model_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SHIPCLASS']._serialized_start=341
  _globals['_SHIPCLASS']._serialized_end=437
  _globals['_ALIGNMENT']._serialized_start=439
  _globals['_ALIGNMENT']._serialized_end=471
  _globals['_COORDINATEREQUEST']._serialized_start=32
  _globals['_COORDINATEREQUEST']._serialized_end=76
  _globals['_OFFICER']._serialized_start=78
  _globals['_OFFICER']._serialized_end=140
  _globals['_SPACESHIP']._serialized_start=143
  _globals['_SPACESHIP']._serialized_end=339
  _globals['_SPACESHIPSERVICE']._serialized_start=473
  _globals['_SPACESHIPSERVICE']._serialized_end=557
# @@protoc_insertion_point(module_scope)
