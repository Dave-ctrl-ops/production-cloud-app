from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool


@app.get("/tasks")
def get_tasks():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, title, description, completed FROM tasks"
    )

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return tasks


@app.post("/tasks")
def create_task(task: Task):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, description)
        VALUES (%s, %s)
        RETURNING id, title, description, completed
        """,
        (task.title, task.description)
    )

    new_task = cursor.fetchone()

    connection.commit()

    cursor.close()
    connection.close()

    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = %s,
            description = %s,
            completed = %s
        WHERE id = %s
        RETURNING id, title, description, completed
        """,
        (task.title, task.description, task.completed, task_id)
    )

    updated_task = cursor.fetchone()

    if updated_task is None:
        cursor.close()
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.commit()

    cursor.close()
    connection.close()

    return updated_task
