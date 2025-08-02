# Little Virtual Library with GUI

import json
import os

from tkinter import *
from tkinter import ttk


root = Tk()
root.title("Your little virtual library")
root.geometry("1024x768")

menu_frame = Frame(root)
add_book_frame = Frame(root)
search_for_book_frame = Frame(root)
display_library_frame = Frame(root)
delete_book_frame = Frame(root)


all_frames = [menu_frame, add_book_frame, search_for_book_frame, display_library_frame, delete_book_frame]

message_label = Label(root, text="", font=("Arial", 14))



def show_frame(frame_to_show):
    for f in all_frames:
        f.pack_forget()
    frame_to_show.pack(pady=20)
    message_label.pack(pady=10)




def read_library_from_file():
    library_file_path = os.path.join(os.path.dirname(__file__), "user_library.json")
    if not os.path.exists(library_file_path):
        with open(library_file_path, "w") as file: # "w" tryb zapisu pliku (czyli tworzenie pliku "user_library.json")
            json.dump([], file)
        return []
    with open(library_file_path, "r") as file: # "r" tryb odczytu z pliku (czyli wyświetlenie zawartości pliku "user_library.json")
        return json.load(file)
    
library = read_library_from_file()

def save_to_file():
    with open("user_library.json", "w") as file:
        json.dump(library, file)
    message_label.config(text="Changes saved successfully!", background="lightgreen", fg="black")


def add_book():
    print("adding book")

def search_books():
    print("Searching for books")

def display_full_library():
    print("Display full library")

def delete_book():
    print("Delete a book")


def build_menu_frame():
    print("Building menu frame")

def build_add_book_frame():
    print("Building add book frame")

def build_search_frame():
    print("Building search frame")

def build_display_library_frame():
    print("Building display library frame")

def build_delete_frame():
    print("Building delete frame")


build_menu_frame()
build_add_book_frame()
show_frame(menu_frame)

root.mainloop()

