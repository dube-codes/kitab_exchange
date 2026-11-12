# Kitab Exchange API

I built this as a personal learning project to practice FastAPI, SQLModel, and SQLite. The app lets me register users and create, list, update, and sell book listings for a college textbook exchange.

## Project overview

This project is a small REST API for managing users and books. I used FastAPI to define the routes and SQLModel to model the database tables.

## Features

- Register a user with a name, email, college, and optional phone number.
- Reject duplicate email registrations.
- Create a book listing linked to a user.
- List unsold books and filter by title and/or author.
- Update a book listing.
- Mark a book as sold.
- Require the `X-API-Key` header on write routes.
- Create the SQLite tables on startup from SQLModel metadata.

## Tech stack

- Python
- FastAPI
- Uvicorn
- SQLModel
- SQLite

## Project structure

```text
.
|-- auth.py
|-- database.py
|-- main.py
|-- models/
|   |-- __init__.py
|   |-- book.py
|   `-- user.py
|-- routes/
|   |-- __init__.py
|   |-- books.py
|   `-- users.py
|-- requirements.txt
|-- README.md
`-- kitab_exchange.db
```

## Database setup and migrations

The database URL is `sqlite:///./kitab_exchange.db` in `database.py`. The app creates the tables at startup by calling `SQLModel.metadata.create_all(engine)` inside `create_tables()`.

There are no migration files and no migration tool in this project. The `Book.user_id` field is linked to `User.id`, and the relationship is defined in the SQLModel models.

## Installation and setup

From the project directory, create a virtual environment and install the dependencies.

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

macOS and Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Environment variables

Not specified in the codebase.

## How to run

```bash
uvicorn main:app --reload
```

The app runs on `http://127.0.0.1:8000` by default.

## API endpoints

The code uses a path parameter named `ver` in the URL, so a request can use a value such as `v1`.

| Method | Path | Description | Authentication |
| --- | --- | --- | --- |
| `GET` | `/` | Return the welcome message. | None |
| `POST` | `/api/{ver}/user/` | Create a user. | `X-API-Key` required |
| `GET` | `/api/{ver}/user/` | List users. | None |
| `GET` | `/api/{ver}/book/` | List unsold books. Optional query params: `title`, `author`. | None |
| `POST` | `/api/{ver}/book/` | Create a book listing. | `X-API-Key` required |
| `PATCH` | `/api/{ver}/book/{book_id}` | Update a book listing. | `X-API-Key` required |
| `PATCH` | `/api/{ver}/book/sold/{book_id}` | Mark a book as sold. | `X-API-Key` required |

The code returns `400` when an email is already registered, `401` for an invalid API key, `404` when a book is not found, and `422` for request validation errors.

## Request and response examples

Create a user with `POST /api/v1/user/`. Send the `X-API-Key` header with your key value.

```json
{
  "name": "Asha Sharma",
  "email": "asha@example.com",
  "phone_number": "9876543210",
  "college": "Delhi University"
}
```

Create a book with `POST /api/v1/book/`.

```json
{
  "title": "Introduction to Economics",
  "author": "Example Author",
  "price": "250",
  "user_id": 1
}
```

Filter books with `GET /api/v1/book/?title=economics&author=Example`.

Update a book with `PATCH /api/v1/book/1`.

```json
{
  "price": "200"
}
```

Mark a book as sold with `PATCH /api/v1/book/sold/1`.

A response from `BookRead` looks like this:

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

A response from `UserRead` contains the following fields:

```json
{
  "id": 1,
  "name": "Asha Sharma",
  "email": "asha@example.com",
  "phone_number": "9876543210",
  "college": "Delhi University",
  "created_at": "2026-01-15T10:30:00+00:00",
  "updated_at": "2026-01-15T10:30:00+00:00"
}
```

## Swagger and OpenAPI docs

FastAPI exposes the interactive docs at `/docs` and `/redoc` when the app is running.

## What I learned

- I defined FastAPI routes and dependencies.
- I modeled tables and validation with SQLModel.
- I used SQLite sessions and startup table creation.
- I added API-key checks with request headers.
- I worked with query filters and patch updates in a REST API.

## Known limitations

- The API key is hard-coded in `auth.py`. It is not loaded from environment variables.
- The POST endpoints return the default FastAPI status code `200` instead of `201`.
- The user list endpoint exposes personal data without authentication.
- `CreateBook.price` and `UpdateBook.price` are strings, but the database model and response model use `int`.
- The app does not validate that `Book.user_id` points to an existing user before inserting a book.
- `UserUpdate` is defined but not used by any route. There is no single-user read or update route.
- The path parameter `ver` is not validated, so any value can be used in the URL.
- No migration workflow or migration files are included in the project.

## Potential improvements

- Move the API key and database URL to environment-based configuration.
- Keep request and stored price values consistent.
- Add read and update routes for a single user.
- Validate the referenced user before creating a book.
- Add automated tests and a migration workflow.
