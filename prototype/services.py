from repositories import UserRepository, BookRepository, LoanRepository


class LibraryError(Exception):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_reader(self, name: str, email: str) -> dict:
        if not name or not email:
            raise LibraryError("Both name and email are required", 400)
        reader = self.user_repo.create(name=name.strip(), email=email.strip())
        return reader.to_dict()

    def list_readers(self) -> list:
        return [r.to_dict() for r in self.user_repo.list_all()]

    def get_reader(self, reader_id: int):
        return self.user_repo.get_by_id(reader_id)


class BookService:
    def __init__(self, book_repo: BookRepository, loan_repo: LoanRepository, user_service: UserService):
        self.book_repo = book_repo
        self.loan_repo = loan_repo
        self.user_service = user_service

    def add_book(self, title: str, author: str) -> dict:
        if not title or not author:
            raise LibraryError("Both title and author are required", 400)
        book = self.book_repo.create(title=title.strip(), author=author.strip())
        return book.to_dict()

    def borrow_book(self, reader_id: int, book_id: int) -> dict:
        if not isinstance(reader_id, int) or not isinstance(book_id, int):
            raise LibraryError("reader_id and book_id must be integers", 400)

        reader = self.user_service.get_reader(reader_id)
        if reader is None:
            raise LibraryError(f"Reader {reader_id} does not exist", 404)

        book = self.book_repo.get_by_id(book_id)
        if book is None:
            raise LibraryError(f"Book {book_id} does not exist", 404)

        if not book.available:
            raise LibraryError(f"Book {book_id} is currently unavailable", 409)

        self.book_repo.update_availability(book_id, False)
        loan = self.loan_repo.create(reader_id=reader_id, book_id=book_id)

        return {
            "loan_id": loan.id,
            "reader_id": reader.id,
            "reader_name": reader.name,
            "book": book.to_dict()
        }
