# Movie Review Web Application

A full-stack web application for movie reviews with Django frontend and Flask RESTful APIs.

## Features

- Django frontend for user interface
- Flask RESTful APIs for data operations
- JWT-based authentication
- CRUD operations for movie reviews
- User authentication and authorization

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with:
```
JWT_SECRET_KEY=your-secret-key-here
```

4. Run database migrations:
```bash
python manage.py migrate
```

## Running the Application

1. Start the Django development server:
```bash
python manage.py runserver
```

2. In a separate terminal, start the Flask API server:
```bash
python run_flask.py
```

The Django frontend will be available at `http://localhost:8000`
The Flask API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- POST `/api/auth/register/` - Register a new user
- POST `/api/auth/login/` - Login and get JWT token

### Reviews
- GET `/api/reviews/` - Get all reviews
- GET `/api/reviews/<id>/` - Get a specific review
- POST `/api/reviews/` - Create a new review
- PUT `/api/reviews/<id>/` - Update a review
- DELETE `/api/reviews/<id>/` - Delete a review

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To use protected endpoints:

1. Register a new user:
```bash
curl -X POST http://localhost:5000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

2. Login to get a token:
```bash
curl -X POST http://localhost:5000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

3. Use the token in subsequent requests:
```bash
curl -X GET http://localhost:5000/api/reviews/ \
  -H "Authorization: Bearer your_token_here"
```

## Deployment

For production deployment:

1. Set up a PostgreSQL database
2. Configure environment variables
3. Use Gunicorn for serving the application
4. Set up Nginx as a reverse proxy
5. Configure SSL certificates

Example Gunicorn command:
```bash
gunicorn movie_review.wsgi:application --bind 0.0.0.0:8000
``` 