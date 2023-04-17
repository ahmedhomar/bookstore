""" A bookstore application using SQLite"""

import sqlite3
from tabulate import tabulate

# Connect to the database
conn = sqlite3.connect("data/ebookstore.db")
# Get a cursor object
cursor = conn.cursor()

# Create a table to store the books: primary key = book id.
conn.execute(
    """CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, author TEXT, qty INTEGER)"""
)

# Inserting records into the database from an inventory file:
def insert_from_file(filename):
    """Insert records into the database from a file"""
    try:
        with open(filename, "r", encoding="utf-8") as reader:
            lines = reader.readlines()
        for line in lines:

            ID, title, author, qty = line.strip().split(";")
            cursor.execute(
                """INSERT OR REPLACE INTO books(id, title, author, qty)
                VALUES(?, ?, ?, ?)""",
                (ID, title, author, qty),
            )
            print(f"\n{title} inserted into database")

    except FileNotFoundError:
        print("File: 'book_inventory.txt' does not exist. Please try again")


# Function to add a book to the database
def add_book(title, author, qty):
    """Adds a book to the database"""
    conn.execute(
        "INSERT INTO books (title, author, qty) VALUES (?, ?, ?)", (title, author, qty)
    )
    conn.commit()
    print("Book added successfully!")


# Function to view all books in the database
def view_books():
    """Prints a table of all books in the database"""
    cursor.execute(
        """SELECT * FROM books""",
    )
    table = cursor.fetchall()
    # Print db table.
    print(
        tabulate(
            table,
            headers=[
                "id",
                "Title",
                "Author",
                "Qty",
            ],
            tablefmt="fancy_grid",
        )
    )


# Function to search for books by title or author
def search_books(search_term):
    """Returns a list of books matching the given search"""
    cursor = conn.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
        (f"%{search_term}%", f"%{search_term}%"),
    )
    # If the search query matched one or more books,
    # search result will be a non-empty list.
    if search_result := list(cursor):
        # Print db table.
        print(
            tabulate(
                search_result,
                headers=[
                    "id",
                    "Title",
                    "Author",
                    "Qty",
                ],
                tablefmt="fancy_grid",
            )
        )
    else:
        print(
            f"\n🫤 No book(s) matching '{search_term}' in the database.Please try again."
        )


# Function to delete a book from the database
def update_qty(qty, book_id):
    """Updates the quantity of a book in the database by id."""
    conn.execute("UPDATE books SET qty = ? WHERE id = ?", (qty, book_id))
    conn.commit()
    print("Book update successfully!")


# Function to delete a book from the database
def delete_book(book_id):
    """Deletes a book from the database by id."""
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")


# ==========Main Menu=============
# Insert initial data in the db from a file.
insert_from_file("book_inventory.txt")
# Program Menu:
MENU = """
** Welcome to Ahmed's Bookstore! **

     .--.                   .---.
   .---|__|           .-.     |~~~|
.--|===|--|_          |_|     |~~~|--.
|  |===|  |'\     .---!~|  .--|   |--|
|%%|   |  |.'\    |===| |--|%%|   |  |
|%%|   |  |\.'\   |   | |__|  |   |  |
|  |   |  | \  \  |===| |==|  |   |  |
|  |   |__|  \.'\ |   |_|__|  |~~~|__|
|  |===|--|   \.'\|===|~|--|%%|~~~|--|
^--^---'--^    `-'`---^-^--^--^---'--' 
(Source: https://www.asciiart.eu/books/books )

M E N U: Please select an option...

a  - Add a book to the database
v  - View all books in the database.
s  - Search for books by title or author.
u  - Update book quantity by book id.
d  - Delete a book from the database by book id.
e  - Exit this program.

"""


# Main program loop
while True:

    # Prompt user to choose from the menu:
    choice = input(MENU).strip().lower()

    if choice == "a":
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        qty = int(input("Enter book qty: "))
        add_book(title, author, qty)
    elif choice == "v":
        view_books()
    elif choice == "s":
        search_term = input("Enter the book title or author name: ")
        search_books(search_term)
    elif choice == "u":
        book_id = int(input("Enter id of the book to update: "))
        qty = int(input("Enter the new book qty: "))
        update_qty(qty, book_id)
    elif choice == "d":
        book_id = int(input("Enter id of the book to delete: "))
        delete_book(book_id)
    elif choice == "e":
        conn.close()
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
