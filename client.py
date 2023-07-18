import socket
import threading
from typing import Protocol

HOST = '127.0.0.1'
PORT = 1234


class Client(Protocol):
    client: socket

    def listen_for_messages_from_server(self, client):
        ...

    def send_message_to_server(self, client):
        ...

    def communicate_to_server(self, client):
        ...


class Client:
    def __init__(self, client: socket):
        self.client = client

    def listen_for_messages_from_server(self, client):
        while 1:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split(":")[0]
                content = message.split(":")[1]
                print(f'[{username}] {content}')
            else:
                print("Message received from client is empty.")

    def send_message_to_server(self, client):
        while 1:
            message = input("Message: ")
            if message != '':
                client.sendall(message.encode())
            else:
                print('Message is empty')
                exit(0)

    def communicate_to_server(self, client):
        username = input("Enter username: ")
        if username != '':
            client.sendall(username.encode())
        else:
            print("Username can not be empty.")
            exit(0)

        threading.Thread(target=self.listen_for_messages_from_server,
                         args=(client, )).start()

        self.send_message_to_server(client)


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_package = Client(client)

    try:
        client.connect((HOST, PORT))
        print(f"Successfully connected to server {HOST}:{PORT}")
    except:
        print(f"Unable to connect to server {HOST}:{PORT}")

    client_package.communicate_to_server(client)


if __name__ == '__main__':
    main()
