# FastAPI URL Shortener

A robust URL shortener service built with FastAPI, PostgreSQL, and SQLAlchemy. This application provides URL shortening with user management, analytics tracking, and API endpoints.

## Features

- **URL Shortening**: Create short, memorable URLs from long ones
- **User Authentication**: JWT-based authentication system
- **Analytics Tracking**: Track clicks, referrers, and user agents
- **User Management**: Register, login, and manage users
- **API Documentation**: Interactive Swagger UI documentation
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Migration Support**: Database migrations using Alembic

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd url-shortener
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```env
DATABASE_URL=postgresql://username:password@localhost/database_name
SECRET_KEY=your-secret-key # Generate using: openssl rand -hex 32
```

5. Initialize the database:
```bash
alembic init alembic
```

6. Run the development server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

### Authentication
- `POST /register` - Register new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user details
- `DELETE /users/{user_id}` - Delete user account

### URL Operations
- `POST /urls/` - Create short URL
- `GET /urls/` - List all URLs for current user
- `GET /urls/{short_code}` - Get URL details
- `GET /urls/{short_code}/redirect` - Redirect to original URL
- `DELETE /urls/{short_code}` - Delete URL

## Usage

1. **Register a New User**
```bash
curl -X POST http://localhost:8000/register \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "username": "username", "password": "password"}'
```

2. **Get Access Token**
```bash
curl -X POST http://localhost:8000/token \
-H "Content-Type: application/json" \
-d '{"username": "username", "password": "password"}'
```

3. **Create a Short URL**
```bash
curl -X POST http://localhost:8000/urls/ \
-H "Authorization: Bearer {access_token}" \
-H "Content-Type: application/json" \
-d '{"original_url": "https://www.example.com"}'
```

## Development

### Database Migrations

1. Create a new migration:
```bash
alembic revision --autogenerate -m "migration_description"
```

2. Apply migrations:
```bash
alembic upgrade head
```

### Running Tests
```bash
pytest
```

## Contributing
1. Fork the repository
2. Create a new branch:
```bash
git checkout -b feature-branch
```
3. Make your changes and commit:
```bash
git add .
git commit -m "Commit message"
```
4. Push to your branch:
```bash
git push origin feature-branch
```
5. Create a pull request

## License
This project is licensed under the MIT License. See the LICENSE file for details.