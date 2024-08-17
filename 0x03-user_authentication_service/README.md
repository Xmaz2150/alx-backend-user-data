# User Authentication Service

This project is a user authentication service built with Flask, SQLAlchemy, and bcrypt. It provides endpoints for user registration, login, profile management, and password reset.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

## Installation

1. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask server:
    ```sh
    python app.py
    ```

2. The server will run on `http://localhost:5000`.

## API Endpoints

### User Registration

- **Endpoint:** `/users`
- **Method:** `POST`
- **Description:** Registers new user.
- **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```

### User Login

- **Endpoint:** `/sessions`
- **Method:** `POST`
- **Description:** Logs user in.
- **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "password123"
    }
    ```

### User Logout

- **Endpoint:** `/sessions`
- **Method:** `DELETE`
- **Description:** Logs user out.
- **Cookies:**
    ```http
    Set-Cookie: session_id=<session_id>
    ```

### User Profile

- **Endpoint:** `/profile`
- **Method:** `GET`
- **Description:** Retrieves user's profile.
- **Cookies:**
    ```http
    Set-Cookie: session_id=<session_id>
    ```

### Password Reset Token

- **Endpoint:** `/reset_password`
- **Method:** `POST`
- **Description:** Generates password reset token.
- **Request Body:**
    ```json
    {
        "email": "user@example.com"
    }
    ```

### Update Password

- **Endpoint:** `/reset_password`
- **Method:** `PUT`
- **Description:** Updates user's password using reset token.
- **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "reset_token": "reset-token",
        "new_password": "newpassword123"
    }
    ```

## Testing

1. Run the tests:
    ```sh
    python main.py
    ```
