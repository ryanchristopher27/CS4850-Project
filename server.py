import socket
import threading

HOST = '127.0.0.1'
PORT = 19786
MAX_CLIENTS = 3

clients = {}  # dictionary to keep track of connected clients

def handle_client(client_socket, client_id):
    # handle client requests
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # send message to specific other client
        message = f"Client {client_id}: {data.decode()}"
        for id, socket in clients.items():
            if id == client_id:
                socket.send(message.encode())
    client_socket.close()
    del clients[client_id]  # remove client from dictionary when it disconnects

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CLIENTS)
    print(f"Server is listening on {HOST}:{PORT}")

    client_id = 1  # start with client ID 1

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        # add new client to dictionary
        clients[client_id] = client_socket

        print("New Client ID: ", client_id)

        # start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        client_thread.start()

        client_id += 1  # increment client ID

if __name__ == '__main__':
    main()
