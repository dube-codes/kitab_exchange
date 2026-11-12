# Kitab Exchange API

Kitab Exchange is a FastAPI REST API for a college textbook exchange. It supports user registration and book listings, including searching available books and marking a listing as sold.

## Features

- Register users with a name, email, college, and optional phone number.
- Reject a registration when the email is already in use.
- Create book listings linked to users.
- List unsold books and filter by title and/or author.
- Update book fields and mark books as sold.
- Protect write endpoints with an API key.
- Create SQLite tables from the SQLModel metadata at application startup.

## Tech Stack

- Python, FastAPI, and Uvicorn
- SQLModel and SQLite

## Project Structure

````text
.
|-- auth.py             # API-key validation
|-- database.py         # SQLite engine, sessions, and table creation
|-- main.py             # FastAPI app and router registration
|-- models/
|   |-- book.py         # Book table and request/response models
|   `-- user.py         # User table and request/response models
|-- routes/
|   |-- books.py        # Book endpoints
|   `-- users.py        # User endpoints
# Kitab Exchange API

Kitab Exchange is a personal learning project: a FastAPI REST API for a college textbook exchange. It supports user registration and book listings, including searching available books and marking listings as sold.

## Features

- Register users with a name, email, college, and optional phone number.
- Reject a registration when the email is already in use.
- Create book listings associated with users.
- List unsold books and filter by title and/or author.
- Update book fields and mark books as sold.
- Protect write endpoints with an API key.
- Create SQLite tables from SQLModel metadata at application startup.

## Tech Stack

- Python
- FastAPI and Uvicorn
- SQLModel and SQLite

## Project Structure

```text
.
|-- auth.py             # API-key validation
|-- database.py         # SQLite engine, sessions, and table creation
|-- main.py             # FastAPI app and router registration
|-- models/
|   |-- book.py         # Book table and request/response models
|   `-- user.py         # User table and request/response models
|-- routes/
|   |-- books.py        # Book endpoints
|   `-- users.py        # User endpoints
|-- requirements.txt    # Python dependencies
`-- README.md
````

## Database Setup and Migrations

The app uses SQLite with the URL `sqlite:///./kitab_exchange.db`, defined in `database.py`. The database file is relative to the process working directory. On startup, `main.py` calls `SQLModel.metadata.create_all()` to create the tables. No migration tool or migration files are present in the project.

`Book.user_id` is a foreign key to `User.id`, and the models define a user-to-books relationship.

## Installation and Setup

From the project directory, create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## How to Run

```bash
uvicorn main:app --reload
```

Uvicorn serves the API at `http://127.0.0.1:8000` by default.

## API Endpoints

Resource routes use a `ver` path segment; the examples below use `v1`. The book-list endpoint accepts optional string query parameters `title` and `author`, which apply substring filters. The book update and sold routes take an integer `book_id` path parameter.

| Method  | Path                             | Description                                                | Authentication       |
| ------- | -------------------------------- | ---------------------------------------------------------- | -------------------- |
| `GET`   | `/`                              | Return the welcome message                                 | None                 |
| `POST`  | `/api/{ver}/user/`               | Register a user                                            | `X-API-Key` required |
| `GET`   | `/api/{ver}/user/`               | List users                                                 | None                 |
| `GET`   | `/api/{ver}/book/`               | List unsold books, optionally filtered by title and author | None                 |
| `POST`  | `/api/{ver}/book/`               | Create a book listing                                      | `X-API-Key` required |
| `PATCH` | `/api/{ver}/book/{book_id}`      | Update book fields                                         | `X-API-Key` required |
| `PATCH` | `/api/{ver}/book/sold/{book_id}` | Mark a book as sold                                        | `X-API-Key` required |

Successful endpoint responses use the default status `200`. Registering an already-used email returns `400`; an invalid API key returns `401`; a missing required API key or invalid request data returns `422`; and updating or marking a nonexistent book returns `404`.

## Request and Response Examples

Register a user with `POST /api/v1/user/`. Include the `X-API-Key` header with your configured key:

```json
{
  "name": "Asha Sharma",
  "email": "asha@example.com",
  "phone_number": "9876543210",
  "college": "Delhi University"
}
```

Create a book with `POST /api/v1/book/`. The request schema declares `price` as a string:

```json
{
  "title": "Introduction to Economics",
  "author": "Example Author",
  "price": "250",
  "user_id": 1
}
```

Filter listings with `GET /api/v1/book/?title=economics&author=Example`.

Update a book with `PATCH /api/v1/book/1` and the `X-API-Key` header. All fields in the update schema are optional:

```json
{
  "price": "200"
}
```

Mark a book as sold with `PATCH /api/v1/book/sold/1` and the `X-API-Key` header. The handler sets `is_sold` to `true`.

A book response has this shape; `price` is an integer in the response schema:

```json
{
  "id": 1,
  "title": "Introduction to Economics",
  "author": "Example Author",
  "price": 250,
  "is_sold": false,
  "user_id": 1,
  "created_at": "2026-01-15T10:30:00+00:00",
  "updated_at": "2026-01-15T10:30:00+00:00"
}
```

User responses contain `id` (integer), `name`, `email`, `phone_number` (string or null), `college`, `created_at`, and `updated_at`. User and book list endpoints return arrays of their corresponding response objects.

## Swagger and OpenAPI

FastAPI's interactive Swagger UI is available at `/docs`, ReDoc at `/redoc`, and the OpenAPI schema at `/openapi.json` on the running server.

## What I Learned

- Defining FastAPI routes and request dependencies.
- Modeling database tables, request/response schemas, foreign keys, and relationships with SQLModel.
- Managing SQLite sessions and creating tables from model metadata.
- Using API-key headers and query parameters in API routes.

## Known Limitations

- The API key is hard-coded in `auth.py`; the project does not load it from an environment variable. Do not publish or reuse the source key.
- Book create and update request schemas declare `price` as a string, while the database model and response schema declare it as an integer.
- `UserUpdate` is defined but not used by an endpoint. There is no single-user lookup or user-update route.
- Book creation does not explicitly check that the supplied `user_id` identifies an existing user before inserting the listing.
- The SQLite schema is created with `create_all()`; no migration workflow is included.

## Potential Improvements

- Load the API key and database URL from environment-based configuration.
- Make book request and stored `price` types consistent.
- Add user retrieval and update routes using the existing user schemas.
- Validate the referenced user when creating a book listing.
- Add automated tests, pagination, and a database migration workflow.
