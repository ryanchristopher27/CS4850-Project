import socket

HOST = '127.0.0.1'
PORT = 19786


def main():

    loggedIn = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client_socket.connect((HOST, PORT))
        print(f"Connected to server at {HOST}:{PORT}")

        while True:
            inp = input(">")
            inpSplit = inp.split(" ")

            # Client not logged in
            if loggedIn == False:
                # Login Function
                if inpSplit[0] == "login":
                    s.sendall(bytes(inp, 'utf-8'))
                    data = s.recv(1024)
                    dataStr = data.decode()
                    print(">" + dataStr)

                    if dataStr == "login confirmed":
                        loggedIn = True
                
                # New User Function
                elif inpSplit[0] == "newuser":
                    # Check length of User ID
                    if len(inpSplit[1]) > 2 and len(inpSplit[1]) < 33:
                        # Check length of User Password
                        if len(inpSplit[2]) > 3 and len(inpSplit[2]) < 9:
                            s.sendall(bytes(inp, 'utf-8'))
                            data = s.recv(1024)
                            dataStr = data.decode()
                            print(">" + dataStr)
                
                # Invalid Input
                else:
                    print("> Denied. Please log in first.")

            # Client logged in
            else:
                # Send Functions
                if inpSplit[0] == "send":
                    lenCheck = -1
                    for val in inpSplit[2:]:
                        lenCheck += len(val) + 1
                    if lenCheck > 0 and lenCheck < 257:
                        s.sendall(bytes(inp, 'utf-8'))
                        data.recv(1024)
                        dataStr = data.decode()
                        print(">" + dataStr)

                # Who Function
                elif inpSplit[0] == "who":
                    s.sendall(bytes(inp, 'utf-8'))
                    data.recv(1024)
                    dataStr = data.decode()
                    print(">" + dataStr)
                
                # Logout Function
                elif inpSplit[0] == "logout":
                    s.sendall(bytes(inp, 'utf-8'))
                    data = s.recv(1024)
                    dataStr = data.decode()
                    print(">" + dataStr)

                # Invalid Input
                else:
                    print("> Error, not a valid input>")


            # recipient = input("Enter recipient ID: ")
            # message = input("Enter a message to send: ")
            # client_socket.send(f"{recipient}:{message}".encode())
            # response = client_socket.recv(1024)
            # print(f"Server response: {response.decode()}")

            # Print response
            
            

if __name__ == '__main__':
    main()
