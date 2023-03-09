# client.py
# Ryan Christopher
# Pawprint: rdcb2f

import socket

def main():
    HOST = "127.0.0.1"
    PORT = 19786  # 1, Last 4 digits of pawprint

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
                        s.sendall(bytes(inp, 'utf-8'))
                        data = s.recv(1024)
                        dataStr = data.decode()
                        print(">" + dataStr)


                # Log Out
                elif inpSplit[0] == "logout":
                    clientOpen = False
                    s.sendall(bytes(inp, 'utf-8'))
                    data = s.recv(1024)
                    dataStr = data.decode()
                    print(">" + dataStr)
                
                # Invalid Input
                else:
                    print("Error, not a valid input")

main()