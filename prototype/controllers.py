from services import UserService, BookService, LibraryError


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self, payload: dict) -> tuple:
        try:
            reader = self.user_service.register_reader(
                name=payload.get("name", ""),
                email=payload.get("email", "")
            )
            return 201, reader
        except LibraryError as exc:
            return exc.status_code, {"error": exc.message}

    def get_users(self) -> tuple:
        readers = self.user_service.list_readers()
        return 200, {"readers": readers}


class BookController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    def create_book(self, payload: dict) -> tuple:
        try:
            book = self.book_service.add_book(
                title=payload.get("title", ""),
                author=payload.get("author", "")
            )
            return 201, book
        except LibraryError as exc:
            return exc.status_code, {"error": exc.message}

    def create_loan(self, payload: dict) -> tuple:
        try:
            result = self.book_service.borrow_book(
                reader_id=payload.get("reader_id"),
                book_id=payload.get("book_id")
            )
            return 201, result
        except LibraryError as exc:
            return exc.status_code, {"error": exc.message}
