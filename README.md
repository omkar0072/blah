# Task API (FastAPI CRUD)

A simple in-memory CRUD API for tasks built with FastAPI.

## Install and run

```bash
pip install -r requirements.txt && uvicorn main:app --reload
```

The API runs at:
- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | API metadata |
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Get one task by id |
| POST | `/tasks` | Create a task (`title`) |
| PUT | `/tasks/{id}` | Update task (`title` and/or `done`) |
| DELETE | `/tasks/{id}` | Delete task |

## Example `curl -i` output

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk"}'
```

Expected response:

```text
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger screenshot

Add a screenshot of `http://127.0.0.1:8000/docs` here after running locally.
