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
    confirm_label = Label(root, text="Changes saved successfully!", font=("Arial", 12), background="lightgreen", fg="black")
    confirm_label.pack(pady=10)
    root.after(2000, confirm_label.destroy)  # Remove the confirmation message after
    




def add_book():
    add_book_message_label.config(text="", fg="black")

    author = entry_author.get().strip()
    title = entry_title.get().strip()
    year = entry_year.get().strip()

    if not author or not title or not year:
        add_book_message_label.config(text="All fields are required!", font=("Arial", 14), fg="red")
        return
    
    if not year.isdigit() or len(year) != 4:
        add_book_message_label.config(text="Year of release must be a 4-digit number. Try again", font=("Arial", 14), fg="red")
        return
    
    new_book = {
        "author" : author,
        "title" : title,
        "year" : year
    }

    library.append(new_book)
    save_to_file()
    clear_add_book_form()

    add_book_message_label.config(text="You can add another book or return to menu.", font=("Arial", 14), fg="green")

    
def search_books(): # do poprawienia wyświetlanie, docelowo uniweralny frame do wyświetlania listy książek
    global result_text
    result_text = ""
    searched_phrase = entry_searched_phrase.get().strip()

    if not searched_phrase:
        search_book_label.config(text="Please enter a title or author to search.", fg="red")
        search_result_label.config(text="")
        return
    
    search_matches = []

    for book in library:
        if searched_phrase.lower() in book['title'].lower() or searched_phrase.lower() in book['author'].lower():
            search_matches.append(book)

    if not search_matches:
        search_book_label.config(text="No books found matching your search.", fg="red")
    else:
        display_books_in_frame(search_for_book_frame, search_matches)

        search_book_label.config(text=result_text.strip(), fg="black")

    clear_search_form()




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
    global add_book_message_label
    global entry_author, entry_title, entry_year

    Label(add_book_frame, text="Author", font=("Arial", 14)).pack(pady=10)
    entry_author = Entry(add_book_frame, font=("Arial", 14))
    entry_author.pack(pady=5)

    Label(add_book_frame, text="Title", font=("Arial", 14)).pack(pady=10)
    entry_title = Entry(add_book_frame, font=("Arial", 14))
    entry_title.pack(pady=5)

    Label(add_book_frame, text="Year of release", font=("Arial", 14)).pack(pady=10)
    entry_year = Entry(add_book_frame, font=("Arial", 14))
    entry_year.pack(pady=5)

    add_book_button = Button(add_book_frame, text="Add book to library", command=add_book, font=("Arial", 14))
    add_book_button.pack(pady=10)
    
    add_book_message_label = Label(add_book_frame, text="Please fill in all fields to add a book to your library", font=("Arial", 16), background="lightblue")
    add_book_message_label.pack(pady=10)

    Button(add_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14)).pack(pady=10)

    clear_add_book_form()


def build_search_frame():
    global entry_searched_phrase, search_book_label, search_result_label

    search_book_label = Label(search_for_book_frame, text="Enter book title or author to search", font=("Arial", 14))
    search_book_label.pack(pady=10)

    search_result_label = Label(search_for_book_frame, text="", font=("Arial", 14), fg="black", background="lightyellow", justify="left")
    search_result_label.pack(pady=10)

    entry_searched_phrase = Entry(search_for_book_frame, font=("Arial", 14))
    entry_searched_phrase.pack(pady=10)

    searching_button =Button(search_for_book_frame, text="Search for book", command=search_books, font=("Arial", 14))
    searching_button.pack(pady=10)

    search_result_label.config(text="Please enter a title or author name to search for.", font=("Arial", 14), fg="black")
    
    Button(search_for_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14)).pack(pady=10)
    clear_search_form()


def build_display_library_frame():
    menu_button = Button(display_library_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14))


def build_delete_frame():
    Button(delete_book_frame, text="Delete book", command=delete_book, font=("Arial", 14))
    clear_delete_form()
    menu_button = Button(delete_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14))





def display_books_in_frame(frame, books): #wygląda lepiej niż gorzej ale jest nierówno
    for widget in frame.winfo_children():
        widget.destroy()

    if not books:
        Label(frame, text="No books to display", font=("Arial", 14), bg="orange").pack(pady=20)
        return
    
    header_frame = Frame(frame, bg="lightblue")
    header_frame.pack(fill=X, pady= (0, 5))

    Label(header_frame, text="AUTHOR", font=("Arial", 14, "bold"), bg="blue",fg="white", width=25, anchor="w").grid(row=0, column=0, padx=5, pady=5)
    Label(header_frame, text="TITLE", font=("Arial", 14, "bold"), bg="blue", fg="white", width=25, anchor="w").grid(row=0, column=1, padx=5, pady=5)
    Label(header_frame, text="YEAR", font=("Arial", 14, "bold"), bg="blue", fg="white", width=10, anchor="w").grid(row=0, column=2, padx=5, pady=5)

    for i, book in enumerate(books, start = 1):
        row_frame = Frame(frame, bg="lightblue")
        row_frame.pack(fill=X, pady=5)

        Label(row_frame, text=book['author'], font=("Arial", 12), bg="lightblue", width=25, anchor="w").grid(row=i, column=0, padx=5, pady=5)
        Label(row_frame, text=book['title'], font=("Arial", 12), bg="lightblue", width=25, anchor="w").grid(row=i, column=1, padx=5, pady=5)
        Label(row_frame, text=book['year'], font=("Arial", 12), bg="lightblue", width=10, anchor="w").grid(row=i, column=2, padx=5, pady=5)

    Button(frame, text="Back to menu", command=lambda: show_frame(menu_frame), font=("Arial", 14)).pack(pady=10)



   


def clear_add_book_form():
    entry_author.delete(0,END)
    entry_title.delete(0, END)
    entry_year.delete(0,END)


def clear_search_form():
    entry_searched_phrase.delete(0, END)
    search_result_label.config(text="")


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

