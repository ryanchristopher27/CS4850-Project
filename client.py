import socket
import select
import sys
import threading

HOST = '127.0.0.1'
PORT = 19786
loggedIn = False
userTemp = ""
user = ""

def constantServerListen(socket):
    global loggedIn
    global user
    global userTemp
    while True:
        data = socket.recv(1024)
        dataStr = data.decode()
        if dataStr == user + " left.":
            break

        print(dataStr)
        # print(">")
        if dataStr == "login confirmed":
            loggedIn = True
            user = userTemp

def main():
    global userTemp

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print("\nMy chat room client. Version Two.\n")

        listenThread = threading.Thread(target=constantServerListen, args=(s,))
        listenThread.start()

        while True:
            inp = input("")
            inpSplit = inp.split(" ")

            # Client not logged in
            if loggedIn == False:
                # Login Function
                if inpSplit[0] == "login":
                    s.sendall(bytes(inp, 'utf-8'))
                    userTemp = inpSplit[1]
                
                # New User Function
                elif inpSplit[0] == "newuser":
                    # Check length of User ID
                    if len(inpSplit[1]) > 2 and len(inpSplit[1]) < 33:
                        # Check length of User Password
                        if len(inpSplit[2]) > 3 and len(inpSplit[2]) < 9:
                            s.sendall(bytes(inp, 'utf-8'))
                
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

                # Who Function
                elif inpSplit[0] == "who":
                    s.sendall(bytes(inp, 'utf-8'))
                
                # Logout Function
                elif inpSplit[0] == "logout":
                    s.sendall(bytes(inp, 'utf-8'))
                    break

                # Invalid Input
                else:
                    print("> Error, not a valid input>")

        listenThread.join()
        
if __name__ == '__main__':
    main()
