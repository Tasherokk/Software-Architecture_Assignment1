# Smart Library Architecture Prototype

**Course:** CSCS5103 Software Architecture (Fall 2026)  
**University:** Kazakh-British Technical University (School of IT and Engineering)  
**Author:** Saduakhas Olzhas  

## Overview

This repository contains a working circulation desk prototype built with a three-layer architecture (**Presentation Layer**, **Business Layer**, and **Data-Access Layer**)[cite: 198]. The prototype demonstrates technical partitioning, closed layers (layer of isolation), high functional cohesion, and low coupling using in-memory storage[cite: 359, 360].

### Project Structure

```text
.
├── models.py          # Domain entities (Reader, Book, Loan dataclasses)
├── repositories.py    # Data-Access Layer (UserRepository, BookRepository, LoanRepository)
├── services.py        # Business Layer (UserService, BookService, LibraryError)
├── controllers.py     # Presentation Layer (UserController, BookController)
├── app.py             # HTTP Server entry point and route dispatcher
└── README.md          # Run instructions and end-to-end API test transcript
```

---

## Architecture & Request Flow

1. **Presentation Layer (`controllers.py`):** `UserController` and `BookController` accept parsed JSON payloads and return `(status_code, response_dict)` tuples without accessing the in-memory stores directly[cite: 359].
2. **Business Layer (`services.py`):** `UserService` and `BookService` enforce circulation rules[cite: 359]. `BookService.borrow_book()` coordinates with `UserService` to verify reader existence before checking and updating book availability[cite: 359].
3. **Data-Access Layer (`repositories.py`):** `UserRepository`, `BookRepository`, and `LoanRepository` encapsulate the in-memory Python dictionaries and lists (`_users`, `_books`, `_loans`)[cite: 359].

---

## Prerequisites & How to Run

* **Prerequisites:** Python 3.9 or newer[cite: 359]. No external packages or third-party dependencies are required (uses Python's built-in `http.server`, `json`, and `dataclasses` modules)[cite: 359].

### Start the Server

Run the following command in the project directory[cite: 359]:

```bash
python app.py
```

Output[cite: 359]:
```text
Smart Library server running on [http://127.0.0.1:8000](http://127.0.0.1:8000)
```

---

## Required REST Endpoints & How to Call Them (`curl`)

Open a second terminal window while the server is running and run the following commands[cite: 359]:

### 1. Register a reader (`POST /users`)
```bash
curl -i -X POST http://127.0.0.1:8000/users -H "Content-Type: application/json" -d "{\"name\": \"Saduakhas Olzhas\", \"email\": \"ol_saduakhas@kbtu.kz\"}"
```

### 2. List registered readers (`GET /users`)
```bash
curl -i -X GET http://127.0.0.1:8000/users
```

### 3. Add a book (`POST /books`)
```bash
curl -i -X POST http://127.0.0.1:8000/books -H "Content-Type: application/json" -d "{\"title\": \"Designing Data-Intensive Applications\", \"author\": \"Martin Kleppmann\"}"
```

### 4. Borrow a book (`POST /loans`)
```bash
curl -i -X POST http://127.0.0.1:8000/loans -H "Content-Type: application/json" -d "{\"reader_id\": 1, \"book_id\": 1}"
```

---

## End-to-End Test Evidence (Request & Response Transcript)

### Step 1: Register a reader (`POST /users`)
**Request:**
```http
POST /users HTTP/1.1
Content-Type: application/json

{"name": "Saduakhas Olzhas", "email": "ol_saduakhas@kbtu.kz"}
```
**Response (`HTTP 201 Created`):**
```json
{
  "id": 1,
  "name": "Saduakhas Olzhas",
  "email": "ol_saduakhas@kbtu.kz"
}
```

### Step 2: List registered readers (`GET /users`)
**Request:**
```http
GET /users HTTP/1.1
```
**Response (`HTTP 200 OK`):**
```json
{
  "readers": [
    {
      "id": 1,
      "name": "Saduakhas Olzhas",
      "email": "ol_saduakhas@kbtu.kz"
    }
  ]
}
```

### Step 3: Add a book (`POST /books`)
**Request:**
```http
POST /books HTTP/1.1
Content-Type: application/json

{"title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"}
```
**Response (`HTTP 201 Created`):**
```json
{
  "id": 1,
  "title": "Designing Data-Intensive Applications",
  "author": "Martin Kleppmann",
  "available": true
}
```

### Step 4: Borrow the book - valid request (`POST /loans`)
**Request:**
```http
POST /loans HTTP/1.1
Content-Type: application/json

{"reader_id": 1, "book_id": 1}
```
**Response (`HTTP 201 Created` - shows book `available` changed to `false`):**
```json
{
  "loan_id": 1,
  "reader_id": 1,
  "reader_name": "Saduakhas Olzhas",
  "book": {
    "id": 1,
    "title": "Designing Data-Intensive Applications",
    "author": "Martin Kleppmann",
    "available": false
  }
}
```

### Step 5: Unsuccessful borrow case 1 - book is already unavailable (`POST /loans`)
**Request:**
```http
POST /loans HTTP/1.1
Content-Type: application/json

{"reader_id": 1, "book_id": 1}
```
**Response (`HTTP 409 Conflict`):**
```json
{
  "error": "Book 1 is currently unavailable"
}
```

### Step 6: Unsuccessful borrow case 2 - unknown reader (`POST /loans`)
**Request:**
```http
POST /loans HTTP/1.1
Content-Type: application/json

{"reader_id": 99, "book_id": 1}
```
**Response (`HTTP 404 Not Found`):**
```json
{
  "error": "Reader 99 does not exist"
}
```