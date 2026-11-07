# TASK MANAGER API

A RESTful API built with FastAPI, SQLAlchemy, and SQLite for managing tasks and categories. It includes JWT authentication, password hashing, and role-based access control.

## Authentication

1. **Sign up:** Send a POST request to `/api/v1/auth/signup` with a username and password.
2. **Log in:** Send a POST request to `/api/v1/auth/login` using your credentials to receive a JWT access token.
3. **Access protected endpoints:** Include the token in your request header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Use the token when calling protected task endpoints. You can also click **Authorize** in Swagger UI (`/docs`) and enter your login credentials.
