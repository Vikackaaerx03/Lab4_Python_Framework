# IP Geolocation API

FastAPI service for laboratory work 4.

## Task coverage

- user registration and authentication
- IP address validation
- geolocation lookup for IP addresses
- saving request history in MongoDB
- HTTP error handling with custom exceptions
- simple frontend for working with the API

## Project structure

```text
app/
|-- routers/
|   |-- auth_router.py
|   |-- lookup_router.py
|   `-- user_router.py
|-- services/
|   |-- auth_service.py
|   |-- lookup_service.py
|   `-- user_service.py
|-- repositories/
|   |-- auth_repository.py
|   |-- lookup_repository.py
|   `-- user_repository.py
|-- models/
|   |-- auth_models.py
|   |-- lookup_models.py
|   `-- user_models.py
|-- core/
|   |-- config.py
|   |-- security.py
|   |-- exceptions.py
|   `-- constants.py
|-- db/
|   `-- database.py
`-- main.py
frontend/
|-- css/
|   `-- style.css
|-- js/
|   `-- app.js
|-- index.html
|-- login.html
|-- register.html
|-- dashboard.html
`-- history.html
```

## Frontend

The frontend is served by FastAPI from the `/frontend` path.

Open in browser:

- `http://127.0.0.1:8000/frontend/index.html`
- `http://127.0.0.1:8000/frontend/login.html`
- `http://127.0.0.1:8000/frontend/register.html`
- `http://127.0.0.1:8000/frontend/dashboard.html`
- `http://127.0.0.1:8000/frontend/history.html`

## Environment variables

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=lab4_ip_geo
SECRET_KEY=change-me
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEO_API_URL=https://ip-api.com/json/{ip}
GEO_TIMEOUT_SECONDS=7
```

## Run

```powershell
cd "C:\Console\visual studio code\python\3 курс\3 курс 2 семестр\Python_framework\Lab4_Python_Framework"
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API endpoints

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `POST /ip/lookup`
- `GET /ip/history`
- `GET /`

## MongoDB collections

- `users`
- `ip_lookups`

## Notes

- invalid IP addresses return a validation error
- lookup service errors return an HTTP error through custom exceptions
- request history stores the user, timestamp, IP, and geolocation data
- the frontend is a simple static UI built with plain HTML, CSS, and JavaScript

