import tkinter as tk
from tkinter import scrolledtext
from typing import Protocol
from dataclasses import dataclass


@dataclass
class Style:
    DARK_GRAY: str = "gray"
    PRIMARY_CLR: str = "orange"
    PRIMARY_CLR_LIGHT: str = "orange"
    WHITE: str = "white"
    FONT_CLR: str = "black"
    FONT = ('Helvetica', 17)
    SMALL_FONT = ('Helvetica', 13)


class GUI_methods(Protocol):
    def send_message_to_chatbox(self):
        ...

    def connect():
        ...

    def send_msg():
        ...


@dataclass
class GUIElements(Protocol):
    root: tk.Tk
    top_frame: tk.Frame
    middle_frame: tk.Frame
    bottom_frame: tk.Frame
    username_label: tk.Label
    username_textbox: tk.Entry
    message_button: tk.Button


class GUI(GUIElements, Style):

    def send_message_to_chatbox(self, message):
        self.message_box.config(state=tk.NORMAL)
        self.message_box.insert(tk.END, message + '\n')
        self.message_box.config(state=tk.DISABLED)

    def connect(self, client_values):
        print("connect btn working!")
        # try:
        #     client_values.client_socket.connect(
        #     (client_values.HOST, client_values.PORT))
        #     print(
        #     f"Successfully connected to server {client_values.HOST}:{client_values.PORT}")
        # except:
        #     print(
        #         f"Unable to connect to server {client_values.HOST}:{client_values.PORT}")
        #     exit(0)

    def send_msg(self):
        print("msg btn working!")

    def __init__(self):
        self.style = Style()
        self.root = tk.Tk()
        self.root.geometry("600x600")
        self.root.title("AetherChat")
        self.root.resizable(False, False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=1)
        self.top_frame = tk.Frame(
            self.root, width=600, height=100, bg=self.style.PRIMARY_CLR)
        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.middle_frame = tk.Frame(
            self.root, width=600, height=400, bg=self.style.DARK_GRAY)
        self.middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.bottom_frame = tk.Frame(
            self.root, width=600, height=100, bg=self.style.PRIMARY_CLR)
        self.bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        self.username_label = tk.Label(
            self.top_frame, text="Username:", font=self.style.FONT, bg=self.style.DARK_GRAY, fg=self.style.WHITE)

        self.username_label.pack(side=tk.LEFT, padx=10)

        self.username_textbox = tk.Entry(
            self.top_frame, font=self.style.FONT, bg=self.style.DARK_GRAY, fg=self.style.WHITE, width=23)
        self.username_textbox.pack(side=tk.LEFT)

        self.username_button = tk.Button(
            self.top_frame, text="Join", font=self.style.FONT, bg=self.style.PRIMARY_CLR, fg=self.style.WHITE, command=self.connect)
        self.username_button.pack(side=tk.LEFT, padx=3)

        self.message_textbox = tk.Entry(
            self.bottom_frame, font=self.style.FONT, bg=self.style.DARK_GRAY, fg=self.style.WHITE, width=33)
        self.message_textbox.pack(side=tk.LEFT, padx=10)

        self.message_button = tk.Button(
            self.bottom_frame, text="Message", font=self.style.FONT, bg=self.style.PRIMARY_CLR, fg=self.style.WHITE, command=self.send_msg)
        self.message_box.config(state=tk.DISABLED)
        self.message_button.pack(side=tk.LEFT, padx=3)

        self.message_box = scrolledtext.ScrolledText(
            self.middle_frame, font=self.style.SMALL_FONT, bg=self.style.PRIMARY_CLR, fg=self.style.WHITE, width=67, height=26.5)
        self.message_box.pack(side=tk.TOP)
        self.root.mainloop()
