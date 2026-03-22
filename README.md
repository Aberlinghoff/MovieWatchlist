# Movie Watchlist API

*A REST API built with FastAPI, SQLAlchemy, JWT Authentication, and TMDB Integration*

---

## Overview

The Movie Watchlist API allows users to register, log in, search for real movies using The Movie Database (TMDB), and manage a personal watchlist. All watchlist data is private — each user can only access their own entries.

---

## Features

- JWT-based user authentication with bcrypt password hashing
- User registration and login with protected endpoints
- Live movie search powered by the TMDB external API
- Personal watchlist management — add, view, and remove movies
- SQLite database with SQLAlchemy ORM
- Auto-generated interactive API docs via Swagger UI

---

## Tech Stack

- **FastAPI** — web framework and routing
- **SQLAlchemy** — ORM and database management
- **SQLite** — local database
- **python-jose** — JWT token creation and validation
- **passlib[bcrypt]** — password hashing
- **httpx** — HTTP client for TMDB API requests
- **python-dotenv** — environment variable management

---

## Project Structure

```
MovieWatchlist/
├── main.py              # App entry point, router registration
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy User and Watchlist models
├── schemas.py           # Pydantic schemas for validation
├── routers/
│   ├── auth.py          # Register and login endpoints
│   ├── movies.py        # Movie search endpoint
│   └── watchlist.py     # Watchlist CRUD endpoints
└── utils/
    ├── auth.py          # Password hashing and JWT utilities
    └── tmdb.py          # TMDB API integration
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/MovieWatchlist.git
cd MovieWatchlist
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install "fastapi[standard]" sqlalchemy python-jose[cryptography] passlib[bcrypt] bcrypt==4.0.1 httpx python-dotenv
```

### 4. Create your .env file

Create a `.env` file in the project root with the following values:

```
SECRET_KEY=your_random_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
TMDB_API_KEY=your_tmdb_api_key_here
```

To generate a secure `SECRET_KEY`, run:

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Get your free TMDB API key at: [themoviedb.org](https://www.themoviedb.org) (Settings > API)

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

Interactive documentation available at `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user account |
| POST | `/auth/login` | Login and receive a JWT token |

### Movies

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/movies/search?query=` | Search for movies via TMDB (public) |

### Watchlist (Protected)

All watchlist endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer your_token_here
```

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/watchlist/` | Add a movie to your watchlist |
| GET | `/watchlist/` | Get your full watchlist |
| DELETE | `/watchlist/{movie_id}` | Remove a movie from your watchlist |

---

## Usage Example

1. Register a new account via `POST /auth/register`
2. Login via `POST /auth/login` — copy the `access_token` from the response
3. Search for a movie via `GET /movies/search?query=inception` — note the movie `id`
4. Add the movie to your watchlist via `POST /watchlist/` with the `movie_id`
5. View your watchlist via `GET /watchlist/`
6. Remove a movie via `DELETE /watchlist/{movie_id}`

All steps can be tested interactively via the Swagger UI at `/docs`.

---

> **Note:** Never commit your `.env` file to version control. Ensure `.env` is listed in your `.gitignore`.
