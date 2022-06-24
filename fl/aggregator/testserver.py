import socket

HOST = '127.0.0.1'
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

server_socket.listen()

count = 0

while True:
    print('Wait...')

    client_socket, addr = server_socket.accept()

    print('Connected by', addr)

    data = client_socket.recv(1024)
    print('Received from', addr, data)

    data = client_socket.recv(1024)
    save_path = '/home/dnclab/dev/Practice/fl/aggregator/received/' + str(count) + '.pickle'
    with open(save_path, 'wb') as f:
        try:
            while data:
                f.write(data)
                data = client_socket.recv(1024)
        except Exception as e:
            print(e)

    count += 1

    client_socket.send('Over'.encode())
    client_socket.close()
    print('Disconnected')

server_socket.close()

print('Server Closed!')

