import terminal

file = open("sharedDirec/.~", "w")
print("direc1"+chr(29)+"D"+chr(29)+"0"+chr(29)+"1"+chr(29), file=file)
file.close()
file = open("sharedDirec/.~"+chr(30)+"direc1", "w")
file.close()

command = terminal.Terminal()

class obj:
    path = ''
    def __init__(self):
        self.command = ""
        self.args = []


command.load_directory(command.absolute_path+command.user_directory)
while True:
    var = input("Enter something:")
    request = obj()
    request.path = var
    if var == "q":
        break
    response = command.cd(request, None)
    command.ls(None, None)
    print(response.pwd)
