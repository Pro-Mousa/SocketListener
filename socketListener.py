import socket

listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  # Use instance multiple times
listener.bind(("10.0.2.10",8080))
listener.listen(0)
print("Listening on port 8080...")

(connection,address) = listener.accept()

print("Listening established..." + str(address))

while True:
    command_input = raw_input("Enter command: ")
    connection.send(command_input)
    command_output = connection.recv(1024)
    print(command_output)