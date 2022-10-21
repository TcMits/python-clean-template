# python-clean-template

## Quick start
Local development:
```sh
# Run app with migrations
docker compose -f local.yml up
```

Production:
```sh
docker compose -f production.yml up
```

Integration tests (can be run in CI):
```sh
docker compose -f integration_test.yml up --abort-on-container-exit --build --exit-code-from http_v1_integration
```

Unit tests (can be run in CI):
```sh
pytest -v --ignore=./integration_test/
```

## Overview

### Web framework
[FastApi](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Database - ORM
[SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

[Alembic](https://alembic.sqlalchemy.org) is a lightweight database migration tool for usage with the [SQLAlchemy](https://www.sqlalchemy.org) Database Toolkit for Python.

### File system
[PyFilesystem](https://docs.pyfilesystem.org/en/latest/introduction.html) is a Python module that provides a common interface to any filesystem. (in future)

### Swagger urls
```
/api/v1/docs
```

### Default urls

----
Login endpoint

* **URL**

  `/api/v1/login`

* **Method:**

  `POST`

* **Data Params**

```json
{
  "username": "string",
  "password": "string"
}
```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{
  "access_token": "string",
  "refresh_token": "string",
  "refresh_key": "string"
}
```

* **Error Response:**

  * **Code:** `400` | `500` | `401` <br />
    **Content:**
```json
{
  "message": "string",
  "code": "string"
  "detail": "string"
}
```


----
Refresh token endpoint

* **URL**

  `/api/v1/refresh-token`

* **Method:**

  `POST`

* **Data Params**

```json
{
  "refresh_token": "string",
  "refresh_key": "string"
}
```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{
  "token": "string"
}
```

* **Error Response:**

  * **Code:** `400` | `500` | `401` <br />
    **Content:**
```json
{
  "message": "string",
  "code": "string",
  "detail": "string"
}
```

----
Verify token endpoint

* **URL**

  `/api/v1/verify-token`

* **Method:**

  `POST`

* **Data Params**

```json
{
  "token": "string"
}
```

* **Success Response:**

  * **Code:** 200 <br />
    **Content:**
```json
{}
```

* **Error Response:**

  * **Code:** `400` | `500` | `401` <br />
    **Content:**
```json
{
  "message": "string",
  "code": "string"
  "detail": "string"

}
```
