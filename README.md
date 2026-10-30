# Bookly – FastAPI Book Review API

A RESTful backend application built using **FastAPI** that provides user authentication, book management, reviews, and tagging functionality.

The project demonstrates backend development concepts including JWT authentication, role-based authorization, asynchronous database operations, Redis-based token revocation, background email processing, and database migrations.

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started – Without Docker](#getting-started--without-docker)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Configure Environment Variables](#4-configure-environment-variables)
  - [5. Set Up PostgreSQL](#5-set-up-postgresql)
  - [6. Set Up Redis](#6-set-up-redis)
  - [7. Run Database Migrations](#7-run-database-migrations)
  - [8. Start the Application](#8-start-the-application)
  - [9. Start the Celery Worker](#9-start-the-celery-worker)
- [Getting Started – With Docker](#getting-started--with-docker)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Background Tasks](#background-tasks)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Features

### Authentication and User Management
- User registration and login.
- Password hashing using bcrypt.
- JWT-based authentication.
- Access token and refresh token mechanism.
- Email verification.
- Password reset functionality.
- Logout with JWT token revocation using Redis.
- Current user information endpoint.

### Book Management
- Create books.
- Retrieve all books.
- Retrieve individual books.
- Retrieve books submitted by a particular user.
- Update book information.
- Delete books.

### Review Management
- Add reviews to books.
- Retrieve all reviews.
- Retrieve individual reviews.
- Delete reviews.

### Tag Management
- Create tags.
- Retrieve available tags.
- Associate tags with books.
- Update tags.
- Delete tags.

### Authorization and Security
- Role-based access control.
- Verified-account checks.
- Protected API endpoints.
- JWT signature and expiration validation.
- Redis-based token blocklisting.

### Background Processing
- Asynchronous email delivery using Celery.
- Redis as the Celery message broker and result backend.

### Database
- PostgreSQL integration.
- Asynchronous database operations.
- SQLModel and SQLAlchemy ORM.
- Database schema migrations using Alembic.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLModel | Database models and ORM |
| SQLAlchemy | Database engine and sessions |
| Alembic | Database migrations |
| Redis | JWT blocklist and Celery broker |
| Celery | Background task processing |
| PyJWT | JWT generation and verification |
| Passlib / bcrypt | Password hashing |
| FastAPI-Mail | Email functionality |
| Uvicorn | ASGI server |

---

## Project Structure

```text
fastapi-project/
│
├── migrations/
│   └── versions/
│
├── src/
│   ├── Auth/
│   │   ├── dependencies.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── utils.py
│   │
│   ├── books/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── service.py
│   │   └── book_data.py
│   │
│   ├── reviews/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── tags/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── service.py
│   │
│   ├── db/
│   │   ├── main.py
│   │   ├── models.py
│   │   └── redis.py
│   │
│   ├── templates/
│   ├── celery_tasks.py
│   ├── config.py
│   ├── errors.py
│   ├── mail.py
│   ├── middleware.py
│   └── __init__.py
│
├── alembic.ini
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Getting Started – Without Docker

This method allows you to run the application directly on your machine without containerizing the application.

## Prerequisites

Install the following software:

1. Python 3.11 or a compatible Python version.
2. PostgreSQL.
3. Redis.
4. Git.

You can download them from:

- Python: https://www.python.org/downloads/
- PostgreSQL: https://www.postgresql.org/download/
- Redis: https://redis.io/download/
- Git: https://git-scm.com/downloads/

Make sure PostgreSQL and Redis are running before starting the application.

## 1. Clone the Repository

Open a terminal and execute:

```bash
git clone https://github.com/Vanshajsingh2203/fastapi-project.git
```

Navigate into the project directory:

```bash
cd fastapi-project
```

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate it.

**Windows (PowerShell):**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```cmd
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

## 3. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a file named `.env` in the root directory of the project.

The application uses Pydantic Settings to load configuration values from this file.

Add the following configuration:

```env
# PostgreSQL Database
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_DB_PASSWORD@localhost:5432/bookly_db

# JWT Configuration
JWT_SECRET_KEY=replace_with_a_secure_random_secret
JWT_ALGORITHM=HS256

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Email Configuration
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com
MAIL_FROM_NAME=Bookly
MAIL_STARTTLS=True
MAIL_SSL_TLS=False
USE_CREDENTIALS=True
VALIDATE_CERTS=True

# Application Domain
DOMAIN=localhost:8000
```

**Important:**

- Replace `YOUR_DB_PASSWORD` with your PostgreSQL password.
- Generate a strong, random JWT secret key.
- Use an email provider's SMTP credentials or app password. Do not use your normal email account password.
- Configure your own SMTP server details if you are not using Gmail.
- Do not commit your `.env` file to GitHub.

The project already includes `.env` in its `.gitignore` file.

## 5. Set Up PostgreSQL

Open PostgreSQL using pgAdmin or the PostgreSQL command-line tool.

Create a database:

```sql
CREATE DATABASE bookly_db;
```

Make sure the database name and credentials match your `DATABASE_URL` in the `.env` file.

The database connection uses the asynchronous PostgreSQL driver `asyncpg`.

## 6. Set Up Redis

Redis is used for:

- Maintaining the JWT token blocklist.
- Acting as the Celery message broker.
- Acting as the Celery result backend.

Start your Redis server.

For a local Redis installation, the default configuration used by the project is:

```env
REDIS_URL=redis://localhost:6379/0
```

Verify that Redis is running:

```bash
redis-cli ping
```

Expected response:

```text
PONG
```

If you are using a different Redis host or port, update `REDIS_URL` accordingly.

## 7. Run Database Migrations

The project uses Alembic to manage database schema changes.

Run:

```bash
alembic upgrade head
```

This applies the available migrations to the configured PostgreSQL database.

Make sure your `.env` file is configured correctly before running this command.

## 8. Start the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn src:app --reload
```

The application will be available at:

```text
http://localhost:8000
```

The `--reload` option automatically restarts the development server when source files change.

## 9. Start the Celery Worker

The application uses Celery for background email processing.

Open a **separate terminal** in the project directory.

Activate the same virtual environment and run:

**Windows:**

```bash
celery -A src.celery_tasks.c_app worker --loglevel=info --pool=solo
```

**Linux / macOS:**

```bash
celery -A src.celery_tasks.c_app worker --loglevel=info
```

Keep the Celery worker running while testing functionality that sends emails through background tasks.

---

# Getting Started – With Docker

Docker is an alternative way to run the application and its supporting services.

The current repository does not yet include a `Dockerfile` or `docker-compose.yml`, so Docker Compose is not currently a ready-to-run setup.

To use this method, Docker support must first be added to the repository.

The intended container setup is:

| Service | Purpose |
|---|---|
| FastAPI | Runs the backend application |
| PostgreSQL | Stores application data |
| Redis | Token blocklist and Celery broker |
| Celery Worker | Processes background email tasks |

Once Docker configuration is added, developers will be able to start the services using:

```bash
docker compose up --build
```

The Docker configuration should also include environment variables, persistent PostgreSQL storage, service dependencies, and a Celery worker.

For now, use the manual installation instructions above.

---

# API Documentation

Once the application is running, FastAPI automatically provides interactive API documentation.

### Swagger UI

```text
http://localhost:8000/api/v1/docs
```

### ReDoc

```text
http://localhost:8000/api/v1/redoc
```

You can use Swagger UI to:

- Explore available API endpoints.
- View request and response schemas.
- Execute API requests.
- Test authentication using JWT access tokens.
- Inspect API responses and status codes.

---

# API Endpoints

All endpoints use the following base URL:

```text
http://localhost:8000/api/v1
```

## Authentication Routes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Authenticate a user |
| GET | `/auth/verify/{token}` | Verify user email |
| GET | `/auth/refresh_token` | Generate a new access token |
| GET | `/auth/me` | Retrieve current user information |
| GET | `/auth/logout` | Revoke the current access token |
| POST | `/auth/send_mail` | Send email through a background task |
| POST | `/auth/password-reset-request` | Request password reset |
| POST | `/auth/password-reset-confirm/{token}` | Reset account password |

## Book Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books/` | Retrieve all books |
| POST | `/books/` | Create a new book |
| GET | `/books/{book_uid}` | Retrieve a particular book |
| GET | `/books/user/{user_uid}` | Retrieve books submitted by a user |
| PATCH | `/books/{book_uid}` | Update book information |
| DELETE | `/books/{book_uid}` | Delete a book |

## Review Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/reviews/` | Retrieve all reviews |
| GET | `/reviews/{review_uid}` | Retrieve a particular review |
| POST | `/reviews/book/{book_uid}` | Add a review to a book |
| DELETE | `/reviews/{review_uid}` | Delete a review |

## Tag Routes

| Method | Endpoint | Description |
|---|---|---|
| GET | `/tags/` | Retrieve all tags |
| POST | `/tags/` | Create a tag |
| POST | `/tags/book/{book_uid}/tags` | Associate tags with a book |
| PUT | `/tags/{tag_uid}` | Update a tag |
| DELETE | `/tags/{tag_uid}` | Delete a tag |

**Note:** Some endpoints require authentication and authorization. Refer to Swagger UI for the request schemas and response details.

---

# Authentication

The application uses JWT (JSON Web Tokens) for authentication.

Two types of tokens are generated during login:

### Access Token

- Used to access protected API endpoints.
- Has a default expiration time of one hour.
- Contains user information and token metadata.

### Refresh Token

- Used to generate a new access token.
- Has an expiration time of two days.

Protected endpoints require an access token in the Authorization header:

```http
Authorization: Bearer <access_token>
```

The application validates JWT signatures and expiration, checks the Redis token blocklist, and applies the relevant authorization dependencies.

Role-based authorization is also implemented to restrict access according to user roles.

---

# Background Tasks

Celery is used to process email-related tasks asynchronously.

Redis acts as the message broker and result backend.

For example, email delivery can be processed in the background rather than making the API request wait for the email operation to finish.

To use these features:

1. Ensure Redis is running.
2. Configure SMTP credentials in `.env`.
3. Start the FastAPI application.
4. Start the Celery worker in a separate terminal.

---

# Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET_KEY` | Secret key used for JWT signing |
| `JWT_ALGORITHM` | JWT signing algorithm |
| `REDIS_URL` | Redis connection URL |
| `MAIL_USERNAME` | SMTP username |
| `MAIL_PASSWORD` | SMTP password or app password |
| `MAIL_FROM` | Sender email address |
| `MAIL_PORT` | SMTP port |
| `MAIL_SERVER` | SMTP server hostname |
| `MAIL_FROM_NAME` | Sender display name |
| `MAIL_STARTTLS` | Enable STARTTLS |
| `MAIL_SSL_TLS` | Enable SSL/TLS |
| `USE_CREDENTIALS` | Enable SMTP authentication |
| `VALIDATE_CERTS` | Validate SMTP certificates |
| `DOMAIN` | Application domain used in verification and reset links |

---

# Troubleshooting

### 1. Database Connection Error

Check that:

- PostgreSQL is running.
- The database exists.
- Your database username and password are correct.
- `DATABASE_URL` is correctly configured.

### 2. Redis Connection Error

Check that Redis is running:

```bash
redis-cli ping
```

Make sure `REDIS_URL` points to the correct Redis instance.

### 3. ModuleNotFoundError

Activate your virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Alembic Migration Error

Make sure:

- PostgreSQL is running.
- The database exists.
- Your `.env` file contains the correct `DATABASE_URL`.
- The migration files are present.

### 5. Emails Are Not Being Sent

Check that:

- SMTP credentials are correct.
- The email provider allows SMTP access.
- Redis is running.
- The Celery worker is running.
- The SMTP server and port are configured correctly.

---

# Contributing

Contributions, suggestions, and improvements are welcome.

If you would like to contribute:

1. Fork this repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Push your branch.
6. Open a Pull Request.

---

## Author

**Vanshaj Singh Bhadauria**

GitHub: [@Vanshajsingh2203](https://github.com/Vanshajsingh2203)

---

If you find this project useful, consider giving the repository a ⭐ on GitHub.

