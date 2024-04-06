import socket
import threading
  
server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
mac_address = "40:a3:cc:7e:f7:1a"
channel = 4
server_sock.bind((mac_address, channel))
server_sock.listen()
print("Server listening...")

clients = []
nicknames = []

def broadcast(message):
    #Broadcast a message to all the clients
    for client in clients:
        print(message)
        client.send(message)

def handle_client(client):
    while True:
        try:
            #Receive messages from client
            message = client.recv(1024)
            broadcast(message)
        except:
            #In case an error occurs (like when a client disconnects), remove the client and nickname from lists
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            client.close()
            broadcast(f"{nickname} has left the chat".encode('utf-8'))
            break

def receive():
    while True:
        client, addr = server_sock.accept()
        print(f"Connection established with {str(addr)}")

        #Send a codeword to notify the connected client to send their nickname
        client.send("S3NDN1CKN4ME".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        #Notify the client and all the others that the connection was successful
        print(f"Client nickname is {nickname}")
        broadcast(f"{nickname} joined the chat".encode('utf-8'))

        #Start a thread that handles the client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
