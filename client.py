import socket
import threading
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

def receive(client_sock, nickname):
    while True:
        try:
            message = client_sock.recv(1024).decode('utf-8')
            if message == "S3NDN1CKN4ME":
                client_sock.send(nickname.encode("utf-8"))
            elif message == "K1CK":
                client_sock.close()
                print(f"{Fore.YELLOW}You got kicked by host")
                break
            else:
                print(message)
        except ConnectionAbortedError:
            print(f"{Fore.YELLOW}{Style.DIM}Connection to server was aborted.")
            client_sock.close()
            break
        except ConnectionResetError:
            print(f"{Fore.YELLOW}{Style.DIM}Connection to server was reset.")
            client_sock.close()
            break
        except OSError as e:
            print(f"{Fore.YELLOW}{Style.DIM}OSError occurred: {e}")
            client_sock.close()
            break


def write(client_sock, nickname):
    while True:
        try:
            user_input = input("")
            if user_input != "":
                if user_input[0] == "/":
                    print(f"{Style.DIM}Only the host can use commands")
                else:
                    message = f"{Fore.LIGHTBLUE_EX}{nickname}: {Fore.RESET}{user_input}".encode("utf-8")
                    client_sock.send(message)
            else:
                print(f"{Style.DIM}You can't send empty messages")

        except ConnectionAbortedError:
            print(f"{Fore.YELLOW}{Style.DIM}Connection to server was aborted.")
            client_sock.close()
            break
        except ConnectionResetError:
            print(f"{Fore.YELLOW}{Style.DIM}Connection to server was reset.")
            client_sock.close()
            break
        except OSError as e:
            print(f"{Fore.YELLOW}{Style.DIM}OSError occurred: {e}")
            client_sock.close()
            break



#main
print(f"{Style.DIM}Configuration needed....")
modes = ["ip", "bt", "bluetooth"]
config = input("Choose between IP (unprotected) or Bluetooth based comunication: ").lower()
while config not in modes:
    config = input("Option not existing (ip, bt, bluetooth): ").lower()

if config == "ip":
    client_sock = socket.socket()
    server_addr = input("Enter server ip address: ")
    while True:
        try:
            port = int(input("Enter port: "))
            break
        except:
           print("Enter a valid number") 

elif (config == "bluetooth") or (config == "bt"):
    client_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server_addr = input("Enter the server's MAC address: ")
    port = 4


nickname = input("Choose your nickname: ")

client_sock.connect((server_addr, port))
print(f'{Fore.YELLOW}{Style.DIM}Connection established!')

receive_thread = threading.Thread(target=receive, args=(client_sock, nickname))
write_thread = threading.Thread(target=write, args=(client_sock, nickname))

receive_thread.start()
write_thread.start()

