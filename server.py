import socket
import threading
import colorama
import uuid
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

def broadcast(message):
    #Broadcast a message to all the clients
    for client in clients:
        if client == "server":
            print(message.decode("utf-8"))
        else:
            client.send(message)

def handle_client(client):
    while True:
        try:
            #Receive messages from client
            message = client.recv(1024)
            if not message:
                break
            else:
                broadcast(message)
        except:
            #In case an error occurs (like when a client disconnects), remove the client and nickname from lists
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            client.close()
            broadcast(f"{Fore.YELLOW}{nickname} has left the chat".encode('utf-8'))
            break

def receive():
    while True:
        client, addr = server_sock.accept()
        print(f"{Fore.YELLOW}{Style.DIM}Connection established with {str(addr)}")

        #Send a codeword to notify the connected client to send their nickname
        client.send("S3NDN1CKN4ME".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        #Notify the client and all the others that the connection was successful
        print(f"{Fore.YELLOW}{Style.DIM}Client nickname is {nickname}")
        broadcast(f"{Fore.YELLOW}{nickname} joined the chat".encode('utf-8'))
  
        #Start a thread that handles the client
        thread_handle = threading.Thread(target=handle_client, args=(client,))
        thread_handle.start()



def write():
    while True:
        user_input = input("")
        if user_input != "":
            if user_input[0] == "/":
                commands_manger(user_input)
            else:
                message = f"{Fore.CYAN}{Style.BRIGHT}(host){Style.NORMAL}{Fore.LIGHTBLUE_EX} {server_nickname}: {Fore.RESET}{user_input}".encode("utf-8")
                broadcast(message)
        else:
            print(f"{Style.DIM}You can't send empty messages")


def commands_manger(command):
    parts = command.split(" ")
    command = parts[0][1:]
    if command == "help":
        help_c()
    elif command == "kick":
        if len(parts) >= 2:
            kick_target = parts[1]
            if kick_target != server_nickname:
                kick(kick_target)
            else:
                print(f"{Style.DIM}You can't kick yourself")
        else:
            print(f"{Style.DIM}Target missing")
    elif command == "address":
        print(f"{Style.DIM}Server MAC address: {server_address}")
    else:
        print(f"{Style.DIM}Invalid command type /help for a list of commands")
    

def kick(nickname):
        if nickname in nicknames:
            index = nicknames.index(nickname)
            client = clients[index]
            clients.pop(index)
            nicknames.pop(index)
            client.send("K1CK".encode("utf-8"))
            broadcast(f"{Fore.YELLOW}{nickname} has been kicked from the chat".encode('utf-8'))
        else:
            print(f"{Style.DIM}User not found")

def help_c():
    print(f'''{Style.DIM}Commands:
/help - Display this message
/kick [nickname] - Kick a user from the chat                
/list - List all the users in the chat''')   


#main
print(f"{Style.DIM}Configuration needed....")
modes = ["ip", "bt", "bluetooth"]
config = input("Choose between IP (unprotected) or Bluetooth based comunication: ").lower()
while config not in modes:
    config = input("Option not existing (ip, bt, bluetooth): ").lower()

if config == "ip":
    server_sock = socket.socket()
    server_address = socket.gethostbyname(socket.gethostname())
    while True:
        try:
            port = int(input("Enter port: "))
            break
        except:
           print("Enter a valid number")
    print(f"{Style.DIM}Server address is {server_address}") 

elif (config == "bluetooth") or (config == "bt"):
    server_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server_address = "40:a3:cc:7e:f7:1a"#':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    port = 4
    print(f"{Style.DIM}Server address: {server_address}") 

clients = []
nicknames = []
server_nickname = input("Choose a nickname for the server: ")
nicknames.append(server_nickname)
clients.append("server")

server_sock.bind((server_address, port))
server_sock.listen()
print(f"{Fore.YELLOW}{Style.DIM}Server listening...")

receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)
receive_thread.start()
write_thread.start()

receive_thread.join()
write_thread.join()
