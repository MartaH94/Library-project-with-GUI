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

def clear_message():
    message_label.config(text="")



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
    message_label.config(text="Welcome to your virtual library!", font=("Arial", 16), background="lightblue", fg="black")
    message_label.pack(pady=10)

    add_book_button = Button(menu_frame, text="Add new book", command=lambda: show_frame(add_book_frame), font=("Arial", 14))
    search_book_button = Button(menu_frame, text="Search for a book", command=lambda: show_frame(search_for_book_frame), font=("Arial", 14))
    display_library_button = Button(menu_frame, text="Display full library", command=lambda: show_frame(display_library_frame), font=("Arial", 14))
    delete_book_button = Button(menu_frame, text="Delete a book", command=lambda: show_frame(delete_book_frame), font=("Arial", 14))
    exit_button = Button(menu_frame, text="Exit library", command=root.quit, font=("Arial", 14))

    add_book_button.pack(pady=10)
    search_book_button.pack(pady=10)
    display_library_button.pack(pady=10)
    delete_book_button.pack(pady=10)
    exit_button.pack(pady=10)


def build_add_book_frame():
    message_label.config(text="Fill all fields to add a book to your library", font=("Arial", 14), background="lightyellow", fg="black")
    message_label.pack(pady=10)

    global entry_author, entry_title, entry_year

    Label(add_book_frame, text="Author", font=("Arial", 14)).pack(pady=10)
    entry_author = Entry(add_book_frame, font=("Arial", 14))
    entry_author.pack(pady=5)

    Label(add_book_frame, text="Title", font=("Arial", 14)).pack(pady=10)
    entry_title = Entry(add_book_frame, font=("Arial", 14))
    entry_title.pack(pady=5)

    Label(add_book_frame, text="Year of release", font=("Arial", 14)).pack(pady=10)
    entry_year = Entry(add_book_frame, font("Arial", 14))
    entry_year.pack(pady=5)

    add_book_button = Button(add_book_frame, text="Add book to library", command=add_book, font=("Arial", 14))
    add_book_button.pack(pady=10)
    
    Button(add_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14)).pack(pady=10)

    clear_add_book_form()

def build_search_frame():
    Button(search_for_book_frame, text="Search for book", command=search_books, font=("Arial", 14))
    clear_search_form()
    menu_button = Button(search_for_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14))


def build_display_library_frame():
    menu_button = Button(display_library_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14))


def build_delete_frame():
    Button(delete_book_frame, text="Delete book", command=delete_book, font=("Arial", 14))
    clear_delete_form()
    menu_button = Button(delete_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14))




def get_add_book_form_data():
    pass

def clear_add_book_form():
    entry_author.delete(0,END)
    entry_title.delete(0, END)
    entry_year.delete(0,END)


def clear_search_form():
    pass

def get_book_to_delete():
    pass

def clear_delete_form():
    pass




build_menu_frame()
build_add_book_frame()
build_search_frame()
build_display_library_frame()
build_delete_frame()
show_frame(menu_frame)

root.mainloop()

