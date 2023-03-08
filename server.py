# echo-server.py

import socket

def main():

    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 19786  # Port to listen on (non-privileged ports are > 1023)

    users = []

    f = open('users.txt', 'r')

    for line in f:
        strip1 = line.strip("(")
        strip2 = strip1.strip(")\n")
        splitLine= strip2.split(", ")

        users.append((splitLine[0], splitLine[1]))

    # print(users)

    serverOpen = True
    currentUser = None

    while serverOpen:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    dataStr = data.decode()

                    # Handle Client Input
                    sData = dataStr.split(" ")

                    # User Log In
                    if sData[0] == "login":
                        userID = sData[1]
                        userPass = sData[2]
                        validLogin = validLoginInfo(users, userID, userPass)
                        if validLogin: # User logged in with correct userID and Password
                            print(userID + " login.")
                            conn.sendall(bytes("login confirmed", 'utf-8'))
                            currentUser = userID
                        else:
                            conn.sendall(bytes("Denied. Username or Password incorrect.", 'utf-8'))
                    
                    # Create New User
                    elif sData[0] == "newuser":
                        userID = sData[1]
                        userPass = sData[2]
                        validUser = validNewUser(users, userID)
                        if validUser: # UserID is not already used
                            users.append(userID, userPass)
                            print("New user account created.")
                            conn.sendall(bytes("New user account created. Please login.", 'utf-8'))
                        else:
                            conn.sendall(bytes("Denied. User account already exists.", 'utf-8'))

                    # Send Message
                    elif sData[0] == "send":
                        message = currentUser + ": " + sData[1]
                        print(message)
                        conn.sendall(bytes(message, 'utf-8]')) 

                    # Log Out
                    elif sData[0] == "logout":
                        serverOpen = False 
                        print(currentUser + " logout.") 
                        conn.sendall(bytes(currentUser + " left.", 'utf-8')) 
                        break       

                    # print(data)
                    # if not data:
                    #     break
                    # conn.sendall(data)
                    # if data == "logout":
                    #     serverOpen = False

# Check if login request was done with correct id and password
def validLoginInfo(users, userID, userPass):
    valid = False
    for user in users:
        if user[0] == userID and user[1] == userPass:
            valid = True

    # Testing
    if valid:
        print("\nvalid")
    else:
        print("\nnot valid")

    return valid

def validNewUser(users, userID):
    valid = True
    for user in users:
        if user[0] == userID:
            valid = False

    return valid



main()