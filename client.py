from cryptography.fernet import Fernet
import socket
import threading
from typing import Protocol
from dataclasses import dataclass
import tkinter as tk
from gui import GUI
from tkinter import messagebox


@dataclass
class ClientValues:
    HOST: str = '127.0.0.1'
    PORT: int = 1234

    def __post_init__(self):
        self.client_socket: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)


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
        self.client_values = client_values
        self.gui = gui
        self.username_button = tk.Button(
            self.gui.top_frame, height=1, text="Join", font=self.gui.style.FONT, bg=self.gui.style.PRIMARY_CLR, fg=self.gui.style.WHITE, command=lambda: self.connect(self.client_values))
        self.username_button.pack(
            side=tk.LEFT, padx=3, pady=(7, 7))

        self.message_button = tk.Button(
            self.gui.bottom_frame, text="Send", height=1, font=self.gui.style.FONT, bg=self.gui.style.PRIMARY_CLR, fg=self.gui.style.WHITE, command=lambda: self.send_msg(self.client_values))
        self.message_button.pack(side=tk.LEFT, padx=3, pady=(7, 7))

        self.encryption_key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.encryption_key)

    def encrypt_message(self, msg):
        msg_bytes = msg.encode()
        encrypted_msg = self.cipher_suite.encrypt(msg_bytes)
        return encrypted_msg

    def decrypt_message(self, encrypted_msg):
        decrypted_msg_bytes = self.cipher_suite.decrypt(encrypted_msg)
        decrypted_msg = decrypted_msg_bytes.decode()
        return decrypted_msg

    def add_message(self, message):
        self.gui.message_box.config(state=tk.NORMAL)
        self.gui.message_box.insert(tk.END, message + '\n')
        self.gui.message_box.config(state=tk.DISABLED)

    def connect(self, client_values,):
        try:

            # Connect to the server
            client_values.client_socket.connect(
                (self.client_values.HOST, self.client_values.PORT))
            print("Successfully connected to server")
            self.add_message("[SERVER] Successfully connected to the server")
        except:
            messagebox.showerror("Unable to connect to server",
                                 f"Unable to connect to server {self.client_values.HOST} {self.client_values.PORT}")

        username = self.gui.username_textbox.get()
        if username != '':
            client_values.client_socket.sendall(username.encode())
        else:
            messagebox.showerror("Invalid username",
                                 "Username cannot be empty")

        threading.Thread(target=self.listen_for_messages_from_server,
                         args=(client_values.client_socket, )).start()

        self.gui.username_textbox.config(state=tk.DISABLED)
        self.username_button.config(state=tk.DISABLED)
        self.send_message_to_server(client_values.client_socket)

    def send_msg(self, client_values):
        message = self.gui.message_textbox.get()
        encrypted_msg = self.encrypt_message(message)
        print(encrypted_msg)
        if encrypted_msg != '':
            client_values.client_socket.sendall(encrypted_msg)
            self.gui.message_textbox.delete(0, len(encrypted_msg))
        else:
            messagebox.showerror("Empty message", "Message cannot be empty")

    def listen_for_messages_from_server(self, client):
        print("listening")
        while 1:
            encrypted_msg = client.recv(2048)
            if encrypted_msg:
                print(encrypted_msg)
                decrypted_msg = self.decrypt_message(encrypted_msg)
                if decrypted_msg:
                    try:
                        print(decrypted_msg)
                        username, content = decrypted_msg.split(":", 1)
                        print(content)
                        self.add_message(f'[{username}] {content}')
                    except ValueError:
                        print("Invalid message format.")
                else:
                    messagebox.showerror(
                        "Error.", "Empty message")


def main():
    # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_values = ClientValues()
    gui = GUI(client_values)
    client = Client(client_values, gui)
    gui.root.mainloop()


if __name__ == '__main__':
    main()
