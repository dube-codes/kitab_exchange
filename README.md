# Kitab Exchange API

Kitab Exchange is a FastAPI REST API for a college textbook exchange. Students can register, create book listings, browse available books, and mark a listing as sold.

## Features

- Register users with a name, email, college, and optional phone number.
- Prevent registering an email address that is already in use.
- Create book listings associated with a user.
- Browse unsold books and filter by title and/or author.
- Update book fields and mark books as sold.
- Require an API key for write operations.
- Create SQLite tables when the application starts.
- Represent the one-to-many relationship between a user and their books.

## Tech Stack

- Python
- FastAPI and Uvicorn
- SQLModel and SQLite
- Pydantic models through SQLModel

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
|-- requirements.txt
`-- README.md
```

## API Endpoints

All resource endpoints include a `ver` path segment. The examples below use `v1`, for example `/api/v1/user/`.

| Method  | Path                             | Description                                                  | API key  |
| ------- | -------------------------------- | ------------------------------------------------------------ | -------- |
| `GET`   | `/`                              | Return a welcome message                                     | No       |
| `POST`  | `/api/{ver}/user/`               | Register a user                                              | Required |
| `GET`   | `/api/{ver}/user/`               | List users                                                   | No       |
| `GET`   | `/api/{ver}/book/`               | List unsold books; optionally filter by `title` and `author` | No       |
| `POST`  | `/api/{ver}/book/`               | Create a book listing                                        | Required |
| `PATCH` | `/api/{ver}/book/{book_id}`      | Update book fields                                           | Required |
| `PATCH` | `/api/{ver}/book/sold/{book_id}` | Mark a book as sold                                          | Required |

Write requests must include the `X-API-Key` header. The API key is currently hard-coded in `auth.py`.

The book list accepts optional string query parameters `title` and `author`; each filters by a substring match. The book update and mark-as-sold routes require an integer `book_id` path parameter.

Successful operations use FastAPI's default `200` response. Registering an already-used email returns `400`; an invalid API key returns `401`; a missing required API key is rejected with `422`; and updating or marking a nonexistent book returns `404`.

### Request Examples

Register a user:

```http
POST /api/v1/user/
X-API-Key: your-api-key
Content-Type: application/json
```

```json
{
  "name": "Asha Sharma",
  "email": "asha@example.com",
  "phone_number": "9876543210",
  "college": "Delhi University"
}
```

Create a book listing:

```http
POST /api/v1/book/
X-API-Key: your-api-key
Content-Type: application/json
```

```json
{
  "title": "Introduction to Economics",
  "author": "Example Author",
  "price": "250",
  "user_id": 1
}
```

Search available listings:

```http
GET /api/v1/book/?title=economics&author=Example
```

Update a book:

```http
PATCH /api/v1/book/1
X-API-Key: your-api-key
Content-Type: application/json
```

```json
{
  "price": "200"
}
```

Mark a book as sold:

```http
PATCH /api/v1/book/sold/1
X-API-Key: your-api-key
```

### Response Examples

User and book create/update endpoints return the corresponding resource. A book response has this shape:

```json
{
  "id": 1,
  "title": "Introduction to Economics",
  "author": "Example Author",
  "price": 250,
  "is_sold": false,
  "user_id": 1,
  "created_at": "2026-11-12T10:00:00+00:00",
  "updated_at": "2026-11-12T10:00:00+00:00"
}
```

The user response includes `id`, `name`, `email`, `phone_number`, `college`, `created_at`, and `updated_at`. The book and user list endpoints return arrays of their respective response objects.

## Database

The project uses SQLite with the connection URL `sqlite:///./kitab_exchange.db`, defined in `database.py`. The database file is created in the working directory when the app is run, and the tables are created at application startup. `Book.user_id` references `User.id`.

## Installation and Setup

From the project directory, create and activate a virtual environment on Windows, then install the dependencies:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the Project

```powershell
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000` by default.

## Swagger and OpenAPI

FastAPI serves interactive Swagger UI at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs), ReDoc at [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc), and the OpenAPI schema at [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json).

## Environment Variables

There are no environment variables currently used by the project. The SQLite URL and API key are defined directly in `database.py` and `auth.py`, respectively.

## Known Limitations

- The API key is hard-coded in `auth.py`; there is no environment-variable configuration.
- The book table and response model use an integer `price`, while the create and update request models declare it as a string.
- `UserUpdate` is defined, but no user update endpoint is implemented. There is also no endpoint to retrieve a single user by ID.
- Book creation accepts a `user_id`, but the route does not explicitly check that the user exists before creating the listing.

## Potential Improvements

- Load the API key and database URL from environment variables.
- Align the book request `price` types with the integer database and response fields.
- Add user update and individual-user retrieval endpoints using the existing user models.
- Validate the referenced user when creating a book listing.
- Add pagination, automated tests, and database migrations.
