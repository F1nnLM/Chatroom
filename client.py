import socket
import threading

client_sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
#40:a3:cc:7e:f7:1a

server_addr = "40:a3:cc:7e:f7:1a" #input("Enter the server's MAC address: ")
channel = 4

client_sock.connect((server_addr, channel))
print('Connection established!')
nickname = input("Choose your nickname: ")

def receive():
    while True:
        try:
            message = client_sock.recv(1024).decode('utf-8')
            if message == "S3NDN1CKN4ME":
                client_sock.send(nickname.encode("utf-8"))
            else:
                print(message)
        except ConnectionAbortedError:
            print("Connection to server was aborted.")
            client_sock.close()
            break
        except ConnectionResetError:
            print("Connection to server was reset.")
            client_sock.close()
            break
        except OSError as e:
            print(f"OSError occurred: {e}")
            client_sock.close()
            break


def write():
    while True:
        try:
            user_input = input("")
            message = f"{nickname}: {user_input}".encode("utf-8")
            client_sock.send(message)
        except ConnectionAbortedError:
            print("Connection to server was aborted.")
            client_sock.close()
            break
        except ConnectionResetError:
            print("Connection to server was reset.")
            client_sock.close()
            break
        except OSError as e:
            print(f"OSError occurred: {e}")
            client_sock.close()
            break


receive_thread = threading.Thread(target=receive)
write_thread = threading.Thread(target=write)

receive_thread.start()
write_thread.start()