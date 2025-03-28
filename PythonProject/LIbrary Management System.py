from abc import ABC, abstractmethod

class LibraryItem(ABC):
    def __init__(self, title, author, item_id):
        self.title = title
        self.author = author
        self._is_borrowed = False  # Encapsulation (private state)
        self.item_id = item_id

    @property
    def is_borrowed(self):
        return self._is_borrowed

    @is_borrowed.setter
    def is_borrowed(self, status):
        if isinstance(status, bool):
            self._is_borrowed = status

    @abstractmethod
    def display_info(self):
        pass  # Must be implemented in subclasses

    def borrow_item(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            print(f"{self.title} has been borrowed.")
        else:
            print(f"Sorry, {self.title} is already borrowed.")

    def return_item(self):
        if self.is_borrowed:
            self.is_borrowed = False
            print(f"{self.title} has been returned.")
        else:
            print(f"{self.title} was not borrowed.")

class Book(LibraryItem):
    def __init__(self, title, author, item_id, pages):
        super().__init__(title, author, item_id)
        self.pages = pages

    def display_info(self):
        print(f"📖 Book: {self.title} by {self.author}, Pages: {self.pages}, Borrowed: {self.is_borrowed}")

class DVD(LibraryItem):
    def __init__(self, title, director, item_id, duration):
        super().__init__(title, director, item_id)
        self.duration = duration  # Duration in minutes

    def display_info(self):
        print(f"📀 DVD: {self.title} by {self.author}, Duration: {self.duration} min, Borrowed: {self.is_borrowed}")

book1 = Book("1984", "George Orwell", 101, 328)
dvd1 = DVD("Inception", "Christopher Nolan", 202, 148)

print("\n--- Library Inventory ---")
book1.display_info()
dvd1.display_info()

print("\n--- Borrowing Items ---")
book1.borrow_item()
dvd1.borrow_item()

print("\n--- After Borrowing ---")
book1.display_info()
dvd1.display_info()

print("\n--- Returning Items ---")
book1.return_item()
dvd1.return_item()

print("\n--- Final State ---")
book1.display_info()
dvd1.display_info()