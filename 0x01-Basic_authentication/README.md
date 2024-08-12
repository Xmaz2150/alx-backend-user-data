# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)


## Authentication

### What is Basic Authentication
A simple authentication scheme built into the HTTP protocol. It involves sending the credentials(username and password) encoded in Base64 as  part of the HTTP request `Authorization` header. The server decodes the header to retrieve the credentials and verifies them to authenticate the user

### How it works with the API
API uses custom `BasicAuth`:
1. **Extract Authorization Header**: The `authorization_header` method in `Auth` extracts the Authorization header from the request.
2. **Extract Base64 Encoded Credentials**: The `extract_base64_authorization_header` method extracts the Base64 encoded credentials from the Authorization header.
3. **Decode Base64 Credentials**: The `decode_base64_authorization_header` method decodes the Base64 encoded credentials to retrieve the username and password.
4. **Extract User Credentials**: The `extract_user_credentials` method extracts the username and password from the decoded string.
5. **Authenticate User**: The `user_object_from_credentials` method retrieves the user object based on the provided credentials.
6. **Authorize Request**: The `current_user` method uses the above methods to authenticate the user and authorize the request.

#### Integration of `Bsic Auth` in frameworks's entrypoint
