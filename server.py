import socket
import threading
from typing import Protocol
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ActiveClients:
    username: str
    client: socket


@dataclass
class ServerConfig:
    server: socket.socket
    HOST: str
    PORT: int
    LISTENER_LIMIT: int
    active_clients: List[ActiveClients]


class ServerMethods(Protocol):

    def listen_for_messages(self, client, username):
        ...

    def send_message_to_client(self, client, message):
        ...

    def send_messages_to_all(self, message):
        ...

    def client_handler(self, client):
        ...


class ServerData():
    HOST = '127.0.0.1'
    PORT = 1234
    LISTENER_LIMIT = 5
    active_clients = []


class Server(ServerConfig):
    server_config: ServerConfig = ServerConfig()

    def listen_for_messages(self, client: socket.socket, username: str):
        while 1:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                final_msg = username + ':' + message
                self.send_messages_to_all(final_msg)
            else:
                print(f'empty message sent from client {username}')

    def send_message_to_client(self, client: socket.socket, message: str):
        client.sendall(message.encode())

    def send_messages_to_all(self, message):
        for user in self.active_clients:
            self.send_message_to_client(user[1], message)

    def client_handler(self, client):
        while 1:
            username = client.recv(2048).decode('utf-8')
            if username != '':
                self.active_clients.append((username, client))
                break
            else:
                print('Missing username.')

        threading.Thread(target=self.listen_for_messages,
                         args=(client, username, )).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data = ServerData()
    server_obj = Server(server_data)
    try:
        server.bind((server_obj.HOST, server_obj.PORT))
        print(f"Running the server on {server_obj.HOST}:{server_obj.PORT}")
    except:
        print(f"Unable to bind to host {server_obj.HOST}:{server_obj.PORT}")

    server.listen(server_obj.LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(
            f"Succesfully connected to client. {address[0]} {address[1]}")

        threading.Thread(target=server_obj.client_handler,
                         args=(client, )).start()


if __name__ == '__main__':
    main()
