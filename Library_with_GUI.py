# Little Virtual Library with GUI

# ===== Importing Libraries =====
import json
import os

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from ttkthemes import ThemedTk

# ===== GUI Setup =====
# (Main window and frame creation)
root = ThemedTk(theme='arc')

root.title("Your little virtual library")
root.geometry("1024x768")

menu_frame = ttk.Frame(root)
add_book_frame = ttk.Frame(root)
search_for_book_frame = ttk.Frame(root)
display_library_frame = ttk.Frame(root)
delete_book_frame = ttk.Frame(root)

all_frames = [menu_frame, add_book_frame, search_for_book_frame, display_library_frame, delete_book_frame]

message_label = ttk.Label(root, text="")

buttons_style = ttk.Style()
buttons_style.configure(
    "General.TButton",
    font=("Helvetica", 12), 
    background="DarkOlive2",
    foreground="black",
    padding=(10, 5)
)

def show_frame(frame_to_show):
    for f in all_frames:
        f.pack_forget()
    frame_to_show.pack(pady=20)
    message_label.pack(pady=10)

def clear_message():
    message_label.config(text="")


# ===== Library Data Handling =====
# (Loading, saving, and storing book data)
library_file_path = os.path.join(os.path.dirname(__file__), "user_library.json")

def read_library_from_file():    
    if not os.path.exists(library_file_path):
        with open(library_file_path, "w") as file: # "w" tryb zapisu pliku (czyli tworzenie pliku "user_library.json")
            json.dump([], file)
        return []
    with open(library_file_path, "r") as file: # "r" tryb odczytu z pliku (czyli wyświetlenie zawartości pliku "user_library.json")
        return json.load(file)
    
library = read_library_from_file()

def save_to_file():
    with open(library_file_path, "w") as file:
        json.dump(library, file)
    confirm_label = ttk.Label(root, text="Changes saved successfully!")
    confirm_label.pack(pady=10)
    root.after(2000, confirm_label.destroy)  # Remove the confirmation message after
    

# ===== Add Book Functions =====
def add_book():
    add_book_message_label.config(text="")

    author = entry_author.get().strip()
    title = entry_title.get().strip()
    year = entry_year.get().strip()

    if not author or not title or not year:
        add_book_message_label.config(text="All fields are required!")
        return
    
    if not year.isdigit() or len(year) != 4:
        add_book_message_label.config(text="Year of release must be a 4-digit number. Try again")
        return
    
    new_book = {
        "author" : author,
        "title" : title,
        "year" : year
    }

    library.append(new_book)
    save_to_file()
    clear_add_book_form()

    add_book_message_label.config(text="You can add another book or return to menu.")

# ===== Search Book Functions =====    
def search_books(): 
    global result_text
    result_text = ""
    searched_phrase = entry_searched_phrase.get().strip()

    if not searched_phrase:
        search_book_label.config(text="Please enter a title or author to search.")
        return
    
    search_matches = []

    for book in library:
        if searched_phrase.lower() in book['title'].lower() or searched_phrase.lower() in book['author'].lower():
            search_matches.append(book)

    if not search_matches:
        search_book_label.config(text="No books found matching your search.", fg="red")
    else:
        display_books_in_frame(tree_frame_search, search_matches)

        search_book_label.config(text=result_text.strip())

    clear_search_form()

# ===== Display Library =====
def display_full_library(library): 
    if not library:
        info_label = ttk.Label(display_library_frame, text="Your library is empty")
        info_label.pack(pady=10)
        return
    
    display_books_in_frame(tree_frame_library, library)
 
# ===== Delete Book Functions =====
def delete_book():
    global library
    if not library:
        info_label = ttk.Label(delete_book_frame, text="Library is empty. Nothing to delete.")
        info_label.pack(pady=10)
        return

    selected_items = tree_frame_delete.tree.selection()

    if not selected_items:
        messagebox.showinfo('Info', 'Please select book(s) to delete')
        return

    items_to_delete = []

    for item_to_delete in selected_items:
        values = tree_frame_delete.tree.item(item_to_delete, "values")

        for i, book in enumerate(library):
            if book['author'] == values[0] and book['title'] == values[1] and book['year'] == values[2]:
                items_to_delete.append(i)
                

    items_to_delete.sort(reverse=True)

    for item_to_delete in items_to_delete:
        library.pop(item_to_delete)

    save_to_file()

    display_books_in_frame(tree_frame_library, library)
    display_books_in_frame(tree_frame_search, library)
    tree_frame_delete.tree = display_books_in_frame(tree_frame_delete, library, selectmode="extended")

def display_updated_library():
    global library
    library = read_library_from_file()
    display_full_library(library)


# ===== GUI Setup =====
def build_menu_frame():
    message_label.config(text="Welcome to your virtual library!")
    message_label.pack(pady=10)

    root.configure(bg="AntiqueWhite1")

    # add_book_button = Button(menu_frame, text="Add new book", command=lambda: show_frame(add_book_frame), font=("Arial", 14))
    add_book_button = ttk.Button(menu_frame, text="Adding book(s)", command=lambda: show_frame(add_book_frame), style="TButton")
    add_book_button.pack(pady=10)

    search_book_button = ttk.Button(menu_frame, text="Search for a book", command=lambda: show_frame(search_for_book_frame), style="TButton")
    search_book_button.pack(pady=10)

    display_library_button = ttk.Button(menu_frame, text="Display full library", command=lambda: (display_updated_library(), show_frame(display_library_frame)), style="TButton")
    display_library_button.pack(pady=10)

    delete_book_button = ttk.Button(menu_frame, text="Delete a book", command=lambda: (display_updated_library(), show_frame(delete_book_frame)), style="TButton")
    delete_book_button.pack(pady=10)

    exit_button = ttk.Button(menu_frame, text="Exit library", command=root.quit, style="TButton")    
    exit_button.pack(pady=10)


def build_add_book_frame():
    global add_book_message_label
    global entry_author, entry_title, entry_year

    author_label = ttk.Label(add_book_frame, text="Author")
    author_label.pack(pady=10)
    entry_author = Entry(add_book_frame, font=("Arial", 14))
    entry_author.pack(pady=5)

    title_label = ttk.Label(add_book_frame, text="Title")
    title_label.pack(pady=10)
    entry_title = Entry(add_book_frame, font=("Arial", 14))
    entry_title.pack(pady=5)

    year_label = ttk.Label(add_book_frame, text="Year of release")
    year_label.pack(pady=10)
    entry_year = Entry(add_book_frame, font=("Arial", 14))
    entry_year.pack(pady=5)

    add_book_button = ttk.Button(add_book_frame, text="Add book to library", command=add_book)
    add_book_button.pack(pady=10)
    
    add_book_message_label = ttk.Label(add_book_frame, text="Please fill in all fields to add a book to your library", font=("Arial", 16), style="TLabel")
    add_book_message_label.pack(pady=10)

    to_menu_button = ttk.Button(add_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame))
    to_menu_button.pack(pady=10)

    clear_add_book_form()


def build_search_frame():
    global entry_searched_phrase, search_book_label, tree_frame_search

    search_book_label = ttk.Label(search_for_book_frame, text="Enter book title or author to search")
    search_book_label.pack(pady=10)

    entry_searched_phrase = ttk.Entry(search_for_book_frame)
    entry_searched_phrase.pack(pady=10)

    searching_button = ttk.Button(search_for_book_frame, text="Search for book", command=search_books)
    searching_button.pack(pady=10)

    tree_frame_search = Frame(search_for_book_frame)
    tree_frame_search.pack(padx=10, pady=10, fill="both", expand=True)
    
    to_menu_button = ttk.Button(search_for_book_frame, text="Back to menu", command=lambda: show_frame(menu_frame))
    to_menu_button.pack(pady=10)
    clear_search_form()


def build_display_library_frame():
    global tree_frame_library

    full_library_label = ttk.Label(display_library_frame, text="This is full list of books in your library")
    full_library_label.pack(pady=10)

    tree_frame_library = Frame(display_library_frame)
    tree_frame_library.pack(padx=10, pady=10, fill="both", expand=True)

    to_menu_button = ttk.Button(display_library_frame, text="Back to menu", command=lambda: show_frame(menu_frame))
    to_menu_button.pack(pady=10)

    
def build_delete_frame(): 
    global tree_frame_delete

    for widget in delete_book_frame.winfo_children():
        widget.destroy()

    delete_book_label = ttk.Label(delete_book_frame, text="Pick the book(s), that you would like to delete.")
    delete_book_label.pack(pady=10)

    tree_frame_delete = Frame(delete_book_frame)
    tree_frame_delete.pack(padx=10, pady=10, fill="both", expand=True)

    display_books_in_frame(tree_frame_delete, library, selectmode="extended")

    deletete_book_button = ttk.Button(delete_book_frame, text="Delete book", command=delete_book)
    deletete_book_button.pack(pady=10)
    to_menu_button = ttk.Button(display_library_frame, text="Back to menu", command=lambda: show_frame(menu_frame))
    to_menu_button.pack(pady=10)
    
    
def display_books_in_frame(frame, books, selectmode="browse"): 
    global tree

    for widget in frame.winfo_children():
        widget.destroy()

    if not books:
        info_label = ttk.Label(frame, text="No books to display")
        info_label.pack(pady=10)
        return
    
    tree = ttk.Treeview(frame, columns=("author", "title", "year"), show="headings" ,height=10, selectmode=selectmode)
    tree.heading('author', text="AUTHOR")
    tree.heading('title', text="TITLE")
    tree.heading('year', text="YEAR")

    tree.column('author', width=300, anchor="w")
    tree.column('title', width=400, anchor="w")
    tree.column('year', width=100, anchor="center")

    for book in books:
        tree.insert('', 'end', values=(book['author'], book['title'], book['year']))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    tree.pack(side="left", fill="both", expand=True)
    frame.tree = tree
    return tree

def clear_add_book_form():
    entry_author.delete(0,END)
    entry_title.delete(0, END)
    entry_year.delete(0,END)

def clear_search_form():
    entry_searched_phrase.delete(0, END)


build_menu_frame()
build_add_book_frame()
build_search_frame()
build_display_library_frame()
build_delete_frame()


show_frame(menu_frame)

root.mainloop()
