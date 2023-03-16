import socket

HOST = '127.0.0.1'
PORT = 19786

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    while True:
        recipient = input("Enter recipient ID: ")
        message = input("Enter a message to send: ")
        client_socket.send(f"{recipient}:{message}".encode())
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")

if __name__ == '__main__':
    main()
