# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: basics.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x62\x61sics.proto\"9\n\nBuyRequest\x12\r\n\x05stock\x18\x01 \x02(\t\x12\x10\n\x08quantity\x18\x02 \x02(\x05\x12\n\n\x02id\x18\x03 \x02(\x05\"\"\n\x12TransactionSummary\x12\x0c\n\x04\x63ost\x18\x01 \x02(\x05\"+\n\x0cHelloRequest\x12\x0c\n\x04\x64\x61te\x18\x01 \x02(\x05\x12\r\n\x05hello\x18\x02 \x01(\t\"9\n\nHelloReply\x12\x14\n\x0crandomNumber\x18\x01 \x02(\x03\x12\x15\n\rserverMessage\x18\x02 \x01(\t23\n\x07Greeter\x12(\n\x08SayHello\x12\r.HelloRequest\x1a\x0b.HelloReply\"\x00\x32<\n\nStockBuyer\x12.\n\x08\x42uyStock\x12\x0b.BuyRequest\x1a\x13.TransactionSummary\"\x00')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'basics_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_BUYREQUEST']._serialized_start=16
  _globals['_BUYREQUEST']._serialized_end=73
  _globals['_TRANSACTIONSUMMARY']._serialized_start=75
  _globals['_TRANSACTIONSUMMARY']._serialized_end=109
  _globals['_HELLOREQUEST']._serialized_start=111
  _globals['_HELLOREQUEST']._serialized_end=154
  _globals['_HELLOREPLY']._serialized_start=156
  _globals['_HELLOREPLY']._serialized_end=213
  _globals['_GREETER']._serialized_start=215
  _globals['_GREETER']._serialized_end=266
  _globals['_STOCKBUYER']._serialized_start=268
  _globals['_STOCKBUYER']._serialized_end=328
# @@protoc_insertion_point(module_scope)
