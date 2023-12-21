
# This script generates the python files from the proto files.
# directory is the directory where the proto files are located.
directory="../protos/"
build_directory="./src/"

python3 -m grpc_tools.protoc -I../protos --python_out=$build_directory --pyi_out=$build_directory --grpc_python_out=$build_directory $directory/*.proto
