# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 19786  # The port used by the server

clientOpen = True
loggedIn = False
while clientOpen:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))

        message = "default"
        inp = input(">")
        inpSplit = inp.split(" ")

        if loggedIn == False:
            # Log In
            if inpSplit[0] == "login":
                # message = inp
                s.sendall(bytes(inp, 'utf-8'))
                data = s.recv(1024)
                dataStr = data.decode()
                print(">" + dataStr)

                # Check if login was successful and set loggedIn flag
                if dataStr == "login confirmed":
                    loggedIn = True


            # Create new user
            elif inpSplit[0] == "newuser":
                # Check length of User ID
                if len(inpSplit[1]) > 2 and len(inpSplit[1]) < 33:
                    # Check length of User Password
                    if len(inpSplit[2]) > 3 and len(inpSplit[2]) < 9:
                        # message = inp
                        s.sendall(bytes(inp, 'utf-8'))
                        data = s.recv(1024)
                        dataStr = data.decode()
                        print(">" + dataStr)
            
            # Invalid Input
            else:
                print("Denied. Please Log In First.")
        else:
            # Send Message
            if inpSplit[0] == "send":
                if len(inpSplit[1]) > 0 and len(inpSplit[1]) < 257:
                    # message = inp
                    s.sendall(bytes(inp, 'utf-8'))
                    data = s.recv(1024)
                    dataStr = data.decode()
                    print(">" + dataStr)


            # Log Out
            elif inpSplit[0] == "logout":
                # message = inp
                clientOpen = False
                s.sendall(bytes(inp, 'utf-8'))
                data = s.recv(1024)
                dataStr = data.decode()
                print(">" + dataStr)
            
            # Invalid Input
            else:
                print("Error, not a valid input")

        # s.connect((HOST, PORT))
        # s.sendall(bytes(message, 'utf-8'))
        # data = s.recv(1024)

    # print(f"Received {data!r}")
