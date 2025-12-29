# StackUnderflow

A Django REST API for a developer Q&A forum, similar to Stack Overflow.

## Features

- User authentication and authorization
- Post questions with categories (Frontend, Backend, Data Analysis, Design, DevOps, Security)
- Answer questions
- Like questions (unique per user per question)
- Search and filter questions by author or content
- Rate limiting (throttling) to prevent abuse
- Pagination for likes
- Custom permissions for owners and admins

## Tech Stack

- Django 5.2-6.0
- Django REST Framework 3.16.1
- Django Filters 25.2
- SQLite database
- Authentication: Basic Auth and Token Auth

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd forum_backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Setup

1. Run migrations:
   ```
   python manage.py migrate
   ```

2. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

3. Run the development server:
   ```
   python manage.py makemigrations
   python manage.py runserver
   ```

The API will be available at http://127.0.0.1:8000/api/forum/

## API Endpoints

### Questions

- GET /api/forum/questions/ - List all questions
- POST /api/forum/questions/ - Create a new question (authenticated)
- GET /api/forum/questions/{id}/ - Get question details
- PUT /api/forum/questions/{id}/ - Update question (owner/admin)
- PATCH /api/forum/questions/{id}/ - Partial update question (owner/admin)
- DELETE /api/forum/questions/{id}/ - Delete question (owner/admin)

### Answers

- GET /api/forum/answers/ - List all answers
- POST /api/forum/answers/ - Create a new answer (authenticated)
- GET /api/forum/answers/{id}/ - Get answer details
- PUT /api/forum/answers/{id}/ - Update answer (owner/admin)
- PATCH /api/forum/answers/{id}/ - Partial update answer (owner/admin)
- DELETE /api/forum/answers/{id}/ - Delete answer (owner/admin)

### Likes

- GET /api/forum/likes/ - List all likes
- POST /api/forum/likes/ - Like a question (authenticated, unique per user/question)
- GET /api/forum/likes/{id}/ - Get like details
- DELETE /api/forum/likes/{id}/ - Unlike a question (owner/admin)

## Usage

### Authentication

To access protected endpoints, include authentication headers:

- Basic Auth: `Authorization: Basic <base64-encoded-credentials>`
- Token Auth: `Authorization: Token <token>`

### Filtering and Searching

- Search questions: `GET /api/forum/questions/?search=<query>`
- Filter by category: `GET /api/forum/questions/?category=<category>`

### Example Request

Create a question:

```
POST /api/forum/questions/
Authorization: Token <your-token>
Content-Type: application/json

{
  "title": "How to use Django REST Framework?",
  "content": "I'm new to DRF and need help getting started.",
  "category": "backend"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request


