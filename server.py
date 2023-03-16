# server.py
# Ryan Christopher
# Pawprint: rdcb2f
# Date: 3/17/2023

# Description: This is the program that runs the server
    # It receives messages from the clients and returns a corresponding output
    # Up to 3 clients are able to connect to this server at all times
    # It utilizes threads to maintain contact with all 3 clients at the same time

import socket
import threading

HOST = '127.0.0.1'
PORT = 19786
MAXCLIENTS = 3

users = []
clientSocketDict = {}  # dictionary to keep track of connected clients
clientUserDict = {}
numOfClients = 0

def handleClient(clientSocket, client_id):
    currentUser = None
    global numOfClients

    while True:
        # Get data from client
        data = clientSocket.recv(1024)
        if not data:
            break
        dataStr = data.decode()
        sData = dataStr.split(" ")


        # User Login Function
        if sData[0] == "login":
            userID = sData[1]
            userPass = sData[2]
            validLogin = validLoginInfo(users, userID, userPass)
            if validLogin: # User logged in with correct userID and Password
                print(userID + " login.")
                # Send message to logged in client
                clientSocket.sendall(bytes("login confirmed", 'utf-8'))

                # Send message to rest of clients
                msg = userID + " joins."
                for id, socket in clientSocketDict.items():
                    if id != client_id:
                        socket.sendall(bytes(msg, 'utf-8'))
                clientUserDict[client_id] = userID
                currentUser = userID
            else:
                clientSocket.sendall(bytes("Denied. Username or Password incorrect.", 'utf-8'))

        # New User Function
        elif sData[0] == "newuser":
            userID = sData[1]
            userPass = sData[2]
            validUser = validNewUser(users, userID)
            if validUser: # UserID is not already used
                users.append((userID, userPass))
                # Create users file if not already created and write users
                f3 = open('users.txt', 'w')
                for user in users:
                    msg = "(" + user[0] + ", " + user[1] + ")\n"
                    f3.write(msg)
                f3.close()

                print("New user account created.")
                clientSocket.sendall(bytes("New user account created. Please login.", 'utf-8'))
            else:
                clientSocket.sendall(bytes("Denied. User account already exists.", 'utf-8'))

        # Send Functions
        elif sData[0] == "send":
            # Send All Function
            if sData[1] == "all":
                msg = dataStr.replace("send all ", "")
                clientMsg = currentUser + ": " + msg
                print(clientMsg)
                # Send message to all other clients
                for id, socket in clientSocketDict.items():
                    if id != client_id:
                        socket.sendall(bytes(clientMsg, 'utf-8'))
            # Send UserID Function
            else:
                rec = sData[1]
                remStr = "send " + sData[1] + " "
                msg = dataStr.replace(remStr, "")
                clientMsg = currentUser + ": " + msg
                serverMsg = currentUser + " (to " + rec + "): " + msg
                print(serverMsg)
                # Send message to specific client
                for id, socket in clientSocketDict.items():
                    if clientUserDict[id] == rec:
                        socket.sendall(bytes(clientMsg, 'utf-8'))
            
        # Who Function
        elif sData[0] == "who":
            msg = ""
            for key in clientUserDict:
                msg = msg + clientUserDict[key] + ", "
            msg = msg.strip(", ")
            clientSocket.send(bytes(msg, 'utf-8'))

        # Logout Function
        elif sData[0] == "logout":
            print(currentUser + " logout.")
            msg = currentUser + " left."
            for id, socket in clientSocketDict.items():
                    socket.sendall(bytes(msg, 'utf-8'))
            currentUser = None
            # Delete client from dictionaries
            del clientSocketDict[client_id]
            del clientUserDict[client_id]
            numOfClients -= 1


# Check if login request was done with correct id and password
def validLoginInfo(users, userID, userPass):
    valid = False
    for user in users:
        if user[0] == userID and user[1] == userPass:
            valid = True

    return valid

def validNewUser(users, userID):
    valid = True
    for user in users:
        if user[0] == userID:
            valid = False

    return valid


def main():
    userFileCreated = True
    global numOfClients

    # Try to open users.txt file
    try:
        f = open('users.txt', 'r')
        for line in f:
            strip1 = line.strip("(")
            strip2 = strip1.strip(")\n")
            splitLine= strip2.split(", ")

            users.append((splitLine[0], splitLine[1]))
        f.close()
    except IOError:
        userFileCreated = False

    # Open server socket
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(MAXCLIENTS)
    print("\nMy chat room server. Version Two.\n")

    client_id = 1

    while True:
        numOfClients += 1
        if numOfClients <= MAXCLIENTS:
            clientSocket, client_address = serverSocket.accept()

            # add new client to dictionary
            clientSocketDict[client_id] = clientSocket

            # start a new thread to handle the client
            clientThread = threading.Thread(target=handleClient, args=(clientSocket, client_id))
            clientThread.start()

            client_id += 1


if __name__ == '__main__':
    main()
