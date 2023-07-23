import tkinter as tk
from tkinter import scrolledtext, messagebox
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
    # Dark and Sinister Colors
    BACKGROUND: str = "#111111"  # Very dark gray
    PRIMARY_CLR: str = "#AA0000"  # Dark red
    PRIMARY_CLR_LIGHT: str = "#880000"  # Darker red
    FONT_CLR: str = "white"
    LISTBOX_BG: str = "#222222"  # Darker gray
    ENTRY_BG: str = "#333333"  # Dark gray
    BUTTON_BG: str = "#AA0000"  # Dark red

    # Fonts
    FONT = ('Helvetica', 17)
    SMALL_FONT = ('Helvetica', 13)

    # Title Font
    TITLE_FONT = ('Arial Black', 24)

    # Button Height and Width
    BUTTON_HEIGHT: int = 2
    BUTTON_WIDTH: int = 10


class GUI_methods(Protocol):
    def send_message_to_chatbox(self):
        ...

    def connect(client_values):
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


class GUI(GUIElements, Style, ):

    def __init__(self, client_values):
        # self.communicate_to_server = client.communicate_to_server
        # self.send_message_to_server = client.send_message_to_server
        self.client_values = client_values
        self.style = Style()
        self.root = tk.Tk()
        self.root.geometry("600x600")
        self.root.title("AetherChat")
        self.root.resizable(False, False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=1)

        # **************************FRAMES**********************************************
        self.top_frame = tk.Frame(
            self.root, width=600, height=100, bg=self.style.BACKGROUND)
        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.middle_frame = tk.Frame(
            self.root, width=600, height=400, bg=self.style.BACKGROUND)
        self.middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        self.bottom_frame = tk.Frame(
            self.root, width=600, height=100, bg=self.style.BACKGROUND)
        self.bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        # *********************LABELS*****************************************************
        self.username_label = tk.Label(
            self.top_frame, text="Username:", font=self.style.FONT, bg=self.style.ENTRY_BG, fg=self.style.WHITE)

        self.username_label.pack(side=tk.LEFT, padx=10)

        # ************************TEXT WINDOW MIDDLE*********************************************

        self.message_box = scrolledtext.ScrolledText(
            self.middle_frame, font=self.style.SMALL_FONT, bg=self.style.LISTBOX_BG, fg=self.style.WHITE, width=67, height=26.5)
        self.message_box.config(state=tk.DISABLED)
        self.message_box.pack(side=tk.TOP)

        # **********************************TEXTBOXES************************************
        self.username_textbox = tk.Entry(
            self.top_frame, font=self.style.FONT, bg=self.style.ENTRY_BG, fg=self.style.WHITE, width=23)
        self.username_textbox.pack(side=tk.LEFT)

        self.message_textbox = tk.Entry(
            self.bottom_frame, font=self.style.FONT, bg=self.style.ENTRY_BG, fg=self.style.WHITE, width=33)
        self.message_textbox.pack(side=tk.LEFT, padx=10)
