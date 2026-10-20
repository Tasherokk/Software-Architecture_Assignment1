import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repositories import UserRepository, BookRepository, LoanRepository
from services import UserService, BookService
from controllers import UserController, BookController

user_repo = UserRepository()
book_repo = BookRepository()
loan_repo = LoanRepository()

user_service = UserService(user_repo)
book_service = BookService(book_repo, loan_repo, user_service)

user_controller = UserController(user_service)
book_controller = BookController(book_service)


class LibraryRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, body: dict):
         payload = json.dumps(body, indent=2).encode("utf-8")
         self.send_response(status_code)
         self.send_header("Content-Type", "application/json")
         self.send_header("Content-Length", str(len(payload)))
         self.end_headers()
         self.wfile.write(payload)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        return json.loads(raw)

    def do_GET(self):
        if self.path == "/users":
            status, response = user_controller.get_users()
            self._send_json(status, response)
        else:
            self._send_json(404, {"error": "Route not found"})

    def do_POST(self):
        try:
            payload = self._read_json()
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON body"})
            return

        if self.path == "/users":
            status, response = user_controller.create_user(payload)
            self._send_json(status, response)
        elif self.path == "/books":
            status, response = book_controller.create_book(payload)
            self._send_json(status, response)
        elif self.path == "/loans":
            status, response = book_controller.create_loan(payload)
            self._send_json(status, response)
        else:
            self._send_json(404, {"error": "Route not found"})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), LibraryRequestHandler)
    print("Smart Library server running on http://127.0.0.1:8000")
    server.serve_forever()
