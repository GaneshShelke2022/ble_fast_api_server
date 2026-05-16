# BLE Mesh Smart Home Backend (FastAPI)

This repository contains a production-ready FastAPI backend for a BLE Mesh Smart Home system. It provides JWT authentication, room/board/device/state management, WebSocket real-time sync, and MySQL persistence.

Quick start

1. Create a Python virtualenv and activate it.

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix
source venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Configure `.env` (already provided with example values). Ensure MySQL server is running and the database `blemeshapp` exists.

4. Run the app (development):

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API Endpoints

- `POST /auth/login` - login (static test credentials: `kipl` / `123`)
- `GET/POST/PUT/DELETE /rooms`
- `GET/POST/PUT/DELETE /boards`
- `GET/POST/PUT/DELETE /devices`
- `GET/POST /states`
- WebSocket: `ws://<host>/ws`

Notes

- Alembic is scaffolded in `alembic/` for migrations; adapt as required.
- For production, run behind an ASGI server (Gunicorn + Uvicorn workers), secure `.env`, and use proper TLS.

Postman example: send `POST /auth/login` with JSON `{ "username": "kipl", "password": "123" }` and use returned `access_token` in `Authorization: Bearer <token>` header for other endpoints.
