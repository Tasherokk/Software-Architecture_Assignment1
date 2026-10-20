from models import Reader, Book, Loan


class UserRepository:
    def __init__(self):
        self._users = {}
        self._next_id = 1

    def create(self, name: str, email: str) -> Reader:
        reader = Reader(id=self._next_id, name=name, email=email)
        self._users[reader.id] = reader
        self._next_id += 1
        return reader

    def list_all(self) -> list:
        return list(self._users.values())

    def get_by_id(self, reader_id: int):
        return self._users.get(reader_id)


class BookRepository:
    def __init__(self):
        self._books = {}
        self._next_id = 1

    def create(self, title: str, author: str) -> Book:
        book = Book(id=self._next_id, title=title, author=author, available=True)
        self._books[book.id] = book
        self._next_id += 1
        return book

    def get_by_id(self, book_id: int):
        return self._books.get(book_id)

    def update_availability(self, book_id: int, available: bool):
        book = self._books.get(book_id)
        if book is not None:
            book.available = available
        return book


class LoanRepository:
    def __init__(self):
        self._loans = []
        self._next_id = 1

    def create(self, reader_id: int, book_id: int) -> Loan:
        loan = Loan(id=self._next_id, reader_id=reader_id, book_id=book_id)
        self._loans.append(loan)
        self._next_id += 1
        return loan
