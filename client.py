import base64
from cryptography.fernet import Fernet, InvalidToken  # Add this import
from cryptography.fernet import Fernet
import socket
import threading
from typing import Protocol
from dataclasses import dataclass
import tkinter as tk
from gui import GUI
from tkinter import messagebox
<<<<<<< HEAD
from cryptography.fernet import Fernet
=======
from server import Server
import ssl
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776


@dataclass
class ClientValues:
    HOST: str = "127.0.0.1"
    PORT: int = 1234

    def __post_init__(self):
<<<<<<< HEAD
        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
=======
        client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_verify_locations(cafile="client_certificate.pem")
        self.client_socket = context.wrap_socket(
            client_socket, server_hostname='localhost')
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776


class ClientInterface(Protocol):
    client_values: ClientValues

    def listen_for_messages_from_server(self, client) -> None:
        ...

    def send_message_to_server(self, client) -> None:
        ...

    def communicate_to_server(self, client) -> None:
        ...


class Client(ClientInterface):
    def __init__(self, client_values, gui):
        # self.key = Fernet.generate_key()
        self.key = "6LXw5qyv-T5FUjw5gyk-t7lYhrnf0WzN1WdAZjO0aDI="
        self.cipher_suite = Fernet(self.key)
        self.client_values = client_values
        self.gui = gui
        self.username_button = tk.Button(
<<<<<<< HEAD
            self.gui.top_frame,
            height=1,
            text="Join",
            font=self.gui.style.FONT,
            bg=self.gui.style.PRIMARY_CLR,
            fg=self.gui.style.WHITE,
            command=lambda: self.connect(self.client_values),
        )
        self.username_button.pack(side=tk.LEFT, padx=3, pady=(7, 7))

        self.message_button = tk.Button(
            self.gui.bottom_frame,
            text="Send",
            height=1,
            font=self.gui.style.FONT,
            bg=self.gui.style.PRIMARY_CLR,
            fg=self.gui.style.WHITE,
            command=lambda: self.send_msg(self.client_values),
        )
=======
            self.gui.top_frame, height=1, text="Join", font=self.gui.style.FONT, bg=self.gui.style.BUTTON_BG, fg=self.gui.style.WHITE, command=lambda: self.connect(self.client_values))
        self.username_button.pack(
            side=tk.LEFT, padx=3, pady=(7, 7))

        self.message_button = tk.Button(
            self.gui.bottom_frame, text="Send", height=1, font=self.gui.style.FONT, bg=self.gui.style.BUTTON_BG, fg=self.gui.style.WHITE, command=lambda: self.send_msg(self.client_values))
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776
        self.message_button.pack(side=tk.LEFT, padx=3, pady=(7, 7))

        self.encryption_key = b'QHwEvyLkqhtl4KbXftzn9Sd1-1ONoT4cx9Qb8tGsf6k='
        self.cipher_suite = Fernet(self.encryption_key)

    def add_message(self, message):
        self.gui.message_box.config(state=tk.NORMAL)
        self.gui.message_box.insert(tk.END, message + "\n")
        self.gui.message_box.config(state=tk.DISABLED)

    def connect(
        self,
        client_values,
    ):
        try:
            # Connect to the server
            client_values.client_socket.connect(
                (self.client_values.HOST, self.client_values.PORT)
            )
            print("Successfully connected to server")
            self.add_message("[SERVER] Successfully connected to the server")
            username = self.gui.username_textbox.get()
            if username != '':
                client_values.client_socket.sendall(username.encode())
            else:
                messagebox.showerror("Invalid username",
                                     "Username cannot be empty")
        except:
            messagebox.showerror(
                "Unable to connect to server",
                f"Unable to connect to server {self.client_values.HOST} {self.client_values.PORT}",
            )

<<<<<<< HEAD
        username = self.gui.username_textbox.get()
        if username != "":
            client_values.client_socket.sendall(username.encode())
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")

        threading.Thread(
            target=self.listen_for_messages_from_server,
            args=(client_values.client_socket,),
        ).start()
=======
        print("THREADING IS REACHED")
        threading.Thread(target=self.listen_for_messages_from_server,
                         args=(client_values.client_socket, )).start()
        print("THREADING IS PASSED")
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776

        self.gui.username_textbox.config(state=tk.DISABLED)
        self.username_button.config(state=tk.DISABLED)

    def send_msg(self, client_values):
        message = self.gui.message_textbox.get()
<<<<<<< HEAD
        if message != "":
            enc_msg = self.cipher_suite.encrypt(message.encode())
            client_values.client_socket.sendall(enc_msg)
=======
        encrypted_msg = self.cipher_suite.encrypt(message.encode())
        if encrypted_msg:
            client_values.client_socket.sendall(encrypted_msg)
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776
            self.gui.message_textbox.delete(0, len(message))
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def listen_for_messages_from_server(self, client):
        print("listening")
        while 1:
<<<<<<< HEAD
            message = client.recv(2048).decode("utf-8")
            if message != "":
                try:
                    username = message.split(":")[0]
                    content = message.split(":")[1]
                    self.add_message(f"[{username}] {content}")
                except:
                    pass
            else:
                messagebox.showerror("Error.", "Message received from client is empty.")
=======
            encrypted_msg = client.recv(2048)

            try:
                decrypted_msg = self.cipher_suite.decrypt(
                    encrypted_msg).decode()
                print(f"client Decrypted message: {decrypted_msg}")

                if decrypted_msg:
                    try:
                        username, content = decrypted_msg.split(":", 1)
                        self.add_message(f'[{username}] {content}')
                    except ValueError:
                        print("Invalid message format.")
                else:
                    messagebox.showerror("Error.", "Empty message")
            except InvalidToken as e:
                print("Invalid token:", e)
                # Handle the error, possibly re-creating the cipher_suite or
                # requesting a new key from the server.
                # For debugging purposes, you can print the encrypted_msg to check its format.
                # print("Encrypted message:", encrypted_msg)
                # Also, make sure the Fernet key used here matches the one used for encryption.
            except Exception as e:
                print("Error during decryption:", e)
>>>>>>> 502400fa7f0077bcbb90202ea77287671ef2c776


def main():
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_values = ClientValues()
    gui = GUI(client_values)
    client = Client(client_values, gui)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
