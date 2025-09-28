# ✅ TODO API (Flask + JWT + UI + PostgreSQL)

## Overview

This is a full-stack Todo application built using Flask. It supports user authentication using JWT tokens, stores data in a PostgreSQL database, and has an HTML UI for managing todos.

## Features

* User registration and login with JWT authentication.
* Add, view, update, and delete todos.
* Frontend templates using HTML and CSS.
* API testing with Postman.
* PostgreSQL database support.

## Prerequisites

* Python 3.9+
* PostgreSQL installed and running
* pip (Python package manager)
* Git
* Optional: Postman for API testing

## Folder Structure

```
todo-api/
├── app.py
├── models.py
├── routes/
│   ├── auth_routes.py
│   └── todo_routes.py
├── templates/
│   ├── login.html
│   ├── register.html
│   └── todos.html
├── static/
│   └── style.css
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/todo-api.git
cd todo-api
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
JWT_SECRET_KEY=your_jwt_secret_key_here
```

5. Create the PostgreSQL database:

```sql
CREATE DATABASE todo_db;
```

6. Initialize the database tables (Python shell or script):

```python
from app import db
from models import User, Todo

db.create_all()
```

## Running the Application

```bash
# Activate virtual environment if not already activated
python app.py
```

Visit `http://127.0.0.1:5000` in your browser to access the UI.

## API Endpoints

### Authentication

* **POST /auth/register** - Register a new user
* **POST /auth/login** - Login and receive a JWT token

### Todos

* **GET /todos/** - Get all todos for the logged-in user
* **POST /todos/** - Create a new todo (requires JWT)
* **PUT /todos/<id>/** - Update a todo (requires JWT)
* **DELETE /todos/<id>/** - Delete a todo (requires JWT)

### Headers for JWT Protected Routes

```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

### Sample JSON for Creating a Todo

```json
{
  "title": "Buy groceries",
  "description": "Milk, Eggs, Bread"
}
```

## Postman Testing

1. Import the API endpoints into Postman.
2. Register a new user using `/auth/register`.
3. Login using `/auth/login` to get the JWT token.
4. Add `Authorization: Bearer <JWT>` header for all todo endpoints.
5. Test CRUD operations for todos.

## UI Usage

* Access login and registration pages at `/login` and `/register`.
* After login, access the todos page to view and manage todos.
* Use the form on the todos page to add new todos.

## GitHub Deployment

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/todo-api.git
git push -u origin main
```

## License

This project is licensed under the MIT License.
