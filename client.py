import socket
import threading
from typing import Protocol
from dataclasses import dataclass
import tkinter as tk
from gui import GUI


@dataclass
class ClientValues:
    HOST: str = '127.0.0.1'
    PORT: int = 1234

    def __post_init__(self):
        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)


class ClientInterface(Protocol):

    def listen_for_messages_from_server(self, client):
        ...

    def send_message_to_server(self, client):
        ...

    def communicate_to_server(self, client):
        ...


class Client(ClientInterface):

    def listen_for_messages_from_server(self, client):
        while 1:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                try:
                    username = message.split(":")[0]
                    content = message.split(":")[1]
                    print(f'[{username}] {content}')
                except:
                    pass
            else:
                print("Message received from client is empty.")

    def send_message_to_server(self, client):
        while 1:
            message = input("\nMessage: ")
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
    gui = GUI()
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_values = ClientValues()
    client = Client()

    try:
        client_values.client_socket.connect(
            (client_values.HOST, client_values.PORT))
        print(
            f"Successfully connected to server {client_values.HOST}:{client_values.PORT}")
    except:
        print(
            f"Unable to connect to server {client_values.HOST}:{client_values.PORT}")
        exit(0)

    client.communicate_to_server(client_values.client_socket)


if __name__ == '__main__':
    main()
