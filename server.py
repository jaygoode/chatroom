import socket
import threading
from typing import Protocol
from dataclasses import dataclass, field
from typing import List, Optional
from cryptography.fernet import Fernet
<<<<<<< HEAD
=======
import ssl
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776


class ServerMethods(Protocol):
    def listen_for_messages(self, client, username):
        ...

    def send_message_to_client(self, client, message):
        ...

    def send_messages_to_all(self, message):
        ...

    def client_handler(self, client):
        ...


@dataclass
class ActiveClients:
    username: str
    client: socket


@dataclass
class ServerData:
    HOST: socket.socket = "127.0.0.1"
    PORT: int = 1234
    LISTENER_LIMIT: int = 5
    active_clients: List[ActiveClients] = field(default_factory=list)
<<<<<<< HEAD
    key: str = "6LXw5qyv-T5FUjw5gyk-t7lYhrnf0WzN1WdAZjO0aDI="
    cipher_suite = Fernet(key)
=======
    # encryption_key = Fernet.generate_key()
    # encryption_key = b'QHwEvyLkqhtl4KbXftzn9Sd1-1ONoT4cx9Qb8tGsf6k='
    encryption_key = Fernet.generate_key()
    cipher_suite = Fernet(encryption_key)
    certificate_file = "server_certificate.pem"
    private_key_file = "server_private_key.pem"

    def __post_init__(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((self.HOST, self.PORT))
            print(f"Running the server on {self.HOST}:{self.PORT}")
        except Exception as e:
            print(
                f"Unable to bind to host {self.HOST}:{self.PORT}. Error: {e}")

        server_socket.listen(self.LISTENER_LIMIT)

        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(
            certfile=self.certificate_file, keyfile=self.private_key_file)
        while 1:
            client, address = server_socket.accept()
            print(
                f"Succesfully connected to client. {address[0]} {address[1]}")
            ssl_connection = context.wrap_socket(client, server_side=True)
            threading.Thread(target=self.client_handler,
                             args=(ssl_connection, )).start()
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776


class Server(ServerData):
    server_config = ServerData

    def get_cipher_suite(self):
        return self.cipher_suite

    def listen_for_messages(self, client: socket.socket, username: str):
        while 1:
<<<<<<< HEAD
            enc_msg = client.recv(2048)
            message = self.cipher_suite.decrypt(enc_msg).decode("utf-8")
            if message != "" or not message.contains(":"):
                final_msg = username + ":" + message
=======
            message = client.recv(2048)
            decrypted_msg = self.server_config.cipher_suite.decrypt(
                message).decode()
            print(f"Received encrypted message: {message}")
            print(f"Decrypted message: {decrypted_msg}")
            if decrypted_msg and not ":" in decrypted_msg:
                final_msg = username + ':' + decrypted_msg
                final_msg = self.cipher_suite.encrypt(final_msg.encode())
                final_msg = final_msg.decode()
                print(f"Decrypted message: {final_msg}")
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776
                self.send_messages_to_all(final_msg)
            else:
                print(f"empty message sent from client {username}")

    def send_message_to_client(self, client: socket.socket, message: str):
        print(f"send_message_to_client message: {message}")
        client.sendall(message.encode())

    def send_messages_to_all(self, message):
        print(f"send_messages_to_all message: {message}")
        for user in self.active_clients:
            self.send_message_to_client(user[1], message)

    def client_handler(self, client):
        while 1:
            username = client.recv(2048).decode("utf-8")
            print(f"[SERVER] {username} has joined the chat.")
            user_joined_msg = f"[SERVER] {username} has joined the chat."
            if username != "":
                self.active_clients.append((username, client))
                self.send_messages_to_all(user_joined_msg)
                break
            else:
                print("Missing username.")

        threading.Thread(
            target=self.listen_for_messages,
            args=(
                client,
                username,
            ),
        ).start()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data = ServerData()
    server_obj = Server()
<<<<<<< HEAD
    try:
        server.bind((server_obj.HOST, server_obj.PORT))
        print(f"Running the server on {server_obj.HOST}:{server_obj.PORT}")
    except:
        print(f"Unable to bind to host {server_obj.HOST}:{server_obj.PORT}")

    server.listen(server_obj.LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Succesfully connected to client. {address[0]} {address[1]}")

        threading.Thread(target=server_obj.client_handler, args=(client,)).start()
=======
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776


if __name__ == "__main__":
    main()
