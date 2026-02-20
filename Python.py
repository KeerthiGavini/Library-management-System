import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tinydb import TinyDB, Query
import re

# Main Library Management System class
class LibraryManagementSystem:
    def __init__(self, root):  # Corrected __init__
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")

        # Connect to TinyDB databases for books and members
        self.books_db = TinyDB('books.json')  # Database for storing books
        self.members_db = TinyDB('members.json')  # Database for storing members
        self.transactions_db = TinyDB('transactions.json')  # Optional for tracking transactions

        # Heading
        self.heading = tk.Label(root, text="Python Library Management System", font=("Helvetica", 16))
        self.heading.pack(pady=10)

        # Book Management Button
        self.book_button = tk.Button(root, text="Manage Books", command=self.book_management, width=30, height=2)
        self.book_button.pack(pady=10)

        # Member Management Button
        self.member_button = tk.Button(root, text="Manage Members", command=self.member_management, width=30, height=2)
        self.member_button.pack(pady=10)

        # Transaction Management Button
        self.transaction_button = tk.Button(root, text="Manage Transactions", command=self.transaction_management, width=30, height=2)
        self.transaction_button.pack(pady=10)

        # User Authentication Button
        self.auth_button = tk.Button(root, text="User Authentication", command=self.user_authentication, width=30, height=2)
        self.auth_button.pack(pady=10)

    # Book Management
    def book_management(self):
        book_menu = tk.Toplevel(self.root)
        book_menu.title("Book Management")
        book_menu.geometry("400x300")

        def add_book():
            title = simpledialog.askstring("Input", "Enter Book Title:")
            author = simpledialog.askstring("Input", "Enter Book Author:")
            genre = simpledialog.askstring("Input", "Enter Book Genre:")
            if title and author and genre:
                self.books_db.insert({'title': title, 'author': author, 'genre': genre})
                messagebox.showinfo("Success", f"Book '{title}' added successfully.")
            else:
                messagebox.showwarning("Error", "All fields are required.")

        def search_book():
            keyword = simpledialog.askstring("Input", "Enter keyword to search:")
            if keyword:
                Book = Query()
                results = self.books_db.search(Book.title.search(keyword, flags=re.IGNORECASE))
                if results:
                    found_books = [book['title'] for book in results]
                    messagebox.showinfo("Search Results", f"Books found: {', '.join(found_books)}")
                else:
                    messagebox.showinfo("Search Results", "No books found.")

        tk.Button(book_menu, text="Add Book", command=add_book).pack(pady=10)
        tk.Button(book_menu, text="Search Book", command=search_book).pack(pady=10)

    # Member Management
    def member_management(self):
        member_menu = tk.Toplevel(self.root)
        member_menu.title("Member Management")
        member_menu.geometry("400x300")

        def register_member():
            name = simpledialog.askstring("Input", "Enter Member Name:")
            if name:
                self.members_db.insert({'name': name, 'books_borrowed': []})
                messagebox.showinfo("Success", f"Member '{name}' registered successfully.")
            else:
                messagebox.showwarning("Error", "Member name is required.")

        def delete_member():
            name = simpledialog.askstring("Input", "Enter Member Name to delete:")
            Member = Query()
            member = self.members_db.search(Member.name == name)
            if member:
                self.members_db.remove(Member.name == name)
                messagebox.showinfo("Success", f"Member '{name}' deleted.")
            else:
                messagebox.showwarning("Error", "Member not found.")

        tk.Button(member_menu, text="Register Member", command=register_member).pack(pady=10)
        tk.Button(member_menu, text="Delete Member", command=delete_member).pack(pady=10)

    # Transaction Management
    def transaction_management(self):
        transaction_menu = tk.Toplevel(self.root)
        transaction_menu.title("Transaction Management")
        transaction_menu.geometry("400x300")

        def borrow_book():
            member_name = simpledialog.askstring("Input", "Enter Member Name:")
            book_title = simpledialog.askstring("Input", "Enter Book Title:")
            Member = Query()
            Book = Query()
            member = self.members_db.search(Member.name == member_name)
            book = self.books_db.search(Book.title == book_title)
            if member and book:
                borrowed_books = member[0]['books_borrowed']
                borrowed_books.append(book_title)
                self.members_db.update({'books_borrowed': borrowed_books}, Member.name == member_name)
                messagebox.showinfo("Success", f"Book '{book_title}' borrowed by {member_name}.")
            else:
                messagebox.showwarning("Error", "Member or Book not found.")

        def return_book():
            member_name = simpledialog.askstring("Input", "Enter Member Name:")
            book_title = simpledialog.askstring("Input", "Enter Book Title:")
            Member = Query()
            member = self.members_db.search(Member.name == member_name)
            if member and book_title in member[0]['books_borrowed']:
                borrowed_books = member[0]['books_borrowed']
                borrowed_books.remove(book_title)
                self.members_db.update({'books_borrowed': borrowed_books}, Member.name == member_name)
                messagebox.showinfo("Success", f"Book '{book_title}' returned by {member_name}.")
            else:
                messagebox.showwarning("Error", "Book not borrowed by this member.")

        tk.Button(transaction_menu, text="Borrow Book", command=borrow_book).pack(pady=10)
        tk.Button(transaction_menu, text="Return Book", command=return_book).pack(pady=10)

    # User Authentication
    def user_authentication(self):
        def login():
            username = simpledialog.askstring("Input", "Enter username:")
            password = simpledialog.askstring("Input", "Enter password:", show="*")
            if username == "admin" and password == "password":
                messagebox.showinfo("Success", "Login Successful!")
            else:
                messagebox.showerror("Error", "Invalid credentials!")

        auth_menu = tk.Toplevel(self.root)
        auth_menu.title("User Authentication")
        auth_menu.geometry("300x200")
        tk.Button(auth_menu, text="Login", command=login).pack(pady=50)

# Main Application
if __name__ == "__main__":  # Corrected main block
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
