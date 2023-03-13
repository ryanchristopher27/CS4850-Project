# server.py
# Ryan Christopher
# Pawprint: rdcb2f

import socket

from _thread import *
import threading

# Global Variables
printLock = threading.Lock()
users = []
# serverOpen = True
loggedInUsers = []
threadCount = 0
maxThreadCount = 3
connns = {}

def main():
    HOST = "127.0.0.1" 
    PORT = 19786  # 1, Last 4 digits of pawprint

    # users = []

    f = open('users.txt', 'r')
    for line in f:
        strip1 = line.strip("(")
        strip2 = strip1.strip(")\n")
        splitLine= strip2.split(", ")

        users.append((splitLine[0], splitLine[1]))
    f.close()

    # while serverOpen:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        printLock.acquire()
        start_new_thread(threaded, (conn,))


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
 
# thread function
def threaded(c):
    currentUser = None
    while True:
        # data = c.recv(1024)
        data = c.recv(2048)
        dataStr = data.decode()

        # Handle Client Input
        sData = dataStr.split(" ")

        # User Log In
        if sData[0] == "login":
            print("\ntest1")
            userID = sData[1]
            userPass = sData[2]
            validLogin = validLoginInfo(users, userID, userPass)
            print("\ntest2")
            if validLogin: # User logged in with correct userID and Password
                print(userID + " login.")
                c.sendall(bytes("login confirmed", 'utf-8'))
                currentUser = userID
                loggedInUsers.append(currentUser)
            else:
                c.sendall(bytes("Denied. Username or Password incorrect.", 'utf-8'))
        
        # Create New User
        elif sData[0] == "newuser":
            userID = sData[1]
            userPass = sData[2]
            validUser = validNewUser(users, userID)
            if validUser: # UserID is not already used
                users.append((userID, userPass))
                print("New user account created.")
                c.sendall(bytes("New user account created. Please login.", 'utf-8'))
            else:
                c.sendall(bytes("Denied. User account already exists.", 'utf-8'))

        # Send Message
        elif sData[0] == "send":
            # Send All
            if sData[1] == "all":
                print("Send All")
            else:
                message = currentUser + ": " + dataStr.strip("send ")
                print(message)
                c.sendall(bytes(message, 'utf-8]')) 

        # Log Out
        elif sData[0] == "logout":
            serverOpen = False 
            print(currentUser + " logout.") 
            c.sendall(bytes(currentUser + " left.", 'utf-8')) 
            f2 = open('users.txt', 'w')
            for user in users:
                msg = "(" + user[0] + ", " + user[1] + ")\n"
                f2.write(msg)
            f2.close()
            loggedInUsers.remove(currentUser)
            # if len(loggedInUsers) == 0:
            #     serverOpen = False

            printLock.release()
            break
 
    # connection closed
    c.close()

main()