# client.py
# Ryan Christopher
# Pawprint: rdcb2f

import socket

# Global Variables
clientOpen = True
loggedIn = False
userID = None

def main():
    HOST = "127.0.0.1"
    PORT = 19786  # 1, Last 4 digits of pawprint

    global clientOpen
    global loggedIn
    global userID

    while clientOpen:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.connect((HOST, PORT))

            message = "default"
            inp = input(">")
            inpSplit = inp.split(" ")

            if loggedIn == False:
                # Log In
                if inpSplit[0] == "login":
                    userID, loggedIn = login(s, inp, inpSplit)


                # Create new user
                elif inpSplit[0] == "newuser":
                    newUser(s, inp, inpSplit)
                
                # Invalid Input
                else:
                    print("Denied. Please Log In First.")
            else:
                # Send Message
                if inpSplit[0] == "send":
                    # Send All Message
                    if inpSplit[1] == "all":
                        print("Send All")
                    # Send Message to Specific User
                    else:
                        print("Send to specific UserID")
                        if inpSplit[1] == userID:
                            s.sendall(bytes(inp, 'utf-8'))
                            data = s.recv(1024)
                            dataStr = data.decode()
                            print(">" + dataStr)

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

def login(socket, inp, inputArgs):
    socket.sendall(bytes(inp, 'utf-8'))
    data = socket.recv(1024)
    dataStr = data.decode()
    print(">" + dataStr)
    # Check if login was successful and set loggedIn flag
    if dataStr == "login confirmed":
        loggedIn = True
        userID = inputArgs[1]
    else:
        loggedIn = False
        userID = None
    return userID, loggedIn

def newUser(socket, inp, inputArgs):
    if len(inputArgs[1]) > 2 and len(inputArgs[1]) < 33:
        # Check length of User Password
        if len(inputArgs[2]) > 3 and len(inputArgs[2]) < 9:
            socket.sendall(bytes(inp, 'utf-8'))
            data = socket.recv(1024)
            dataStr = data.decode()
            print(">" + dataStr)

main()