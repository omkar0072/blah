from fastapi import Body, FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="Task API", version="1.0")

tasks = [
    {"id": 1, "title": "Learn FastAPI basics", "done": False},
    {"id": 2, "title": "Build CRUD endpoints", "done": False},
    {"id": 3, "title": "Test with curl", "done": True},
]


def find_task(task_id: int):
    return next((task for task in tasks if task["id"] == task_id), None)


@app.get("/", summary="Get API metadata")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Check API health")
def read_health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", summary="Get one task by id")
def get_task(task_id: int):
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )
    return task


@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(payload: dict = Body(default={})):
    title = payload.get("title")
    if not isinstance(title, str) or not title.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "title is required and must be a non-empty string"},
        )

    new_task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": title.strip(),
        "done": False,
    }
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}", summary="Update an existing task")
def update_task(task_id: int, payload: dict = Body(default={})):
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )

    if not payload:
        return JSONResponse(
            status_code=400,
            content={"error": "request body must include title and/or done"},
        )

    if "title" not in payload and "done" not in payload:
        return JSONResponse(
            status_code=400,
            content={"error": "request body must include title and/or done"},
        )

    if "title" in payload:
        title = payload.get("title")
        if not isinstance(title, str) or not title.strip():
            return JSONResponse(
                status_code=400,
                content={
                    "error": "title must be a non-empty string when provided"
                },
            )
        task["title"] = title.strip()

    if "done" in payload:
        done = payload.get("done")
        if not isinstance(done, bool):
            return JSONResponse(
                status_code=400, content={"error": "done must be a boolean when provided"}
            )
        task["done"] = done

    return task


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task")
def delete_task(task_id: int):
    task = find_task(task_id)
    if not task:
        return JSONResponse(
            status_code=404, content={"error": f"Task {task_id} not found"}
        )
    tasks.remove(task)
    return Response(status_code=204)
