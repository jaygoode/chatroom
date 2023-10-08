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
from cryptography.fernet import Fernet


@dataclass
class ClientValues:
    HOST: str = "127.0.0.1"
    PORT: int = 1234

    def __post_init__(self):
        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )


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
        self.message_button.pack(side=tk.LEFT, padx=3, pady=(7, 7))

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
        except:
            messagebox.showerror(
                "Unable to connect to server",
                f"Unable to connect to server {self.client_values.HOST} {self.client_values.PORT}",
            )

        username = self.gui.username_textbox.get()
        if username != "":
            enc_username = self.cipher_suite.encrypt(username.encode())
            client_values.client_socket.sendall(enc_username)
        else:
            messagebox.showerror("Invalid username", "Username cannot be empty")

        threading.Thread(
            target=self.listen_for_messages_from_server,
            args=(client_values.client_socket,),
        ).start()

        self.gui.username_textbox.config(state=tk.DISABLED)
        self.username_button.config(state=tk.DISABLED)

    def send_msg(self, client_values):
        message = self.gui.message_textbox.get()
        if message != "":
            enc_msg = self.cipher_suite.encrypt(message.encode())
            client_values.client_socket.sendall(enc_msg)
            self.gui.message_textbox.delete(0, len(message))
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def listen_for_messages_from_server(self, client):
        print("listening")
        while 1:
            enc_msg = client.recv(2048)
            print(f"enc_msg_client: {enc_msg}")
            message = self.cipher_suite.decrypt(enc_msg)
            print(f"de_enc_msg_client: {message}")
            if message != "":
                try:
                    # username = message.split(":")[0]
                    # content = message.split(":")[1]
                    # self.add_message(f"[{username}] {content}")
                    self.add_message(f"{message}")
                except:
                    pass
            else:
                messagebox.showerror("Error.", "Message received from client is empty.")


def main():
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_values = ClientValues()
    gui = GUI(client_values)
    client = Client(client_values, gui)
    gui.root.mainloop()


if __name__ == "__main__":
    main()
