import tkinter as tk
from random import shuffle

class LibraryGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Game App")
        self.root.geometry("800x600")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        self.books = [
            {"title": "Book 1", "author": "Author 1"},
            {"title": "Book 2", "author": "Author 2"},
            {"title": "Book 3", "author": "Author 3"},
            {"title": "Book 4", "author": "Author 4"},
            {"title": "Book 5", "author": "Author 5"},
        ]

        self.book_list = tk.Listbox(self.frame)
        self.book_list.pack(fill="both", expand=True)

        self.add_book_button = tk.Button(self.frame, text="Add Book", command=self.add_book)
        self.add_book_button.pack()

        self.remove_book_button = tk.Button(self.frame, text="Remove Book", command=self.remove_book)
        self.remove_book_button.pack()

        self.shuffle_books_button = tk.Button(self.frame, text="Shuffle Books", command=self.shuffle_books)
        self.shuffle_books_button.pack()

        self.display_books()

    def display_books(self):
        self.book_list.delete(0, tk.END)
        for book in self.books:
            self.book_list.insert(tk.END, f"{book['title']} by {book['author']}")

    def add_book(self):
        self.add_book_window = tk.Toplevel(self.root)
        self.add_book_window.title("Add Book")

        self.title_label = tk.Label(self.add_book_window, text="Title:")
        self.title_label.pack()

        self.title_entry = tk.Entry(self.add_book_window)
        self.title_entry.pack()

        self.author_label = tk.Label(self.add_book_window, text="Author:")
        self.author_label.pack()

        self.author_entry = tk.Entry(self.add_book_window)
        self.author_entry.pack()

        self.add_button = tk.Button(self.add_book_window, text="Add", command=self.add_book_to_list)
        self.add_button.pack()

    def add_book_to_list(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        self.books.append({"title": title, "author": author})
        self.display_books()
        self.add_book_window.destroy()

    def remove_book(self):
        try:
            selected_index = self.book_list.curselection()[0]
            self.books.pop(selected_index)
            self.display_books()
        except IndexError:
            pass

    def shuffle_books(self):
        shuffle(self.books)
        self.display_books()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGameApp(root)
    root.mainloop()