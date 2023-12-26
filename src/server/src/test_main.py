
import grpc
import Terminal_pb2_grpc as Terminal_pb2_grpc
import Terminal_pb2 as Terminal_pb2
import logging

# file = open("sharedDirec/.~", "w")
# print("direc1"+chr(29)+"D"+chr(29)+"0"+chr(29)+"1"+chr(29), file=file)
# file.close()
# file = open("sharedDirec/.~"+chr(30)+"direc1", "w")
# file.close()

# command = terminal.Terminal()

# class obj:
#     path = ''
#     def __init__(self):
#         self.command = ""
#         self.args = []


# command.load_directory(command.absolute_path+command.user_directory)
# while True:
#     var = input("Enter something:")
#     request = obj()
#     request.path = var
#     if var == "q":
#         break
#     response = command.cd(request, None)
#     command.ls(None, None)
#     print(response.pwd)


def run():
    
    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = Terminal_pb2_grpc.TerminalStub(channel)
        while True:
            inp = input("Entere something: ")
            if inp == "q":
                break
            response = stub.cd(Terminal_pb2.CD(path=inp))
            print(response.pwd)
        
        print("Recieved response: " + response.message + " {response.alive}")
        
    # print("Greeter client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()
