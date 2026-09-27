from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from database import get_connection

app = FastAPI()


@app.get("/health")
def health_check():
    connection = get_connection()
    connection.close()

    return {"status": "healthy"}


class Task(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=500)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or whitespace")

        return value


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(max_length=500)
    completed: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or whitespace")

        return value


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


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = %s
        RETURNING id, title, description, completed
        """,
        (task_id,)
    )

    deleted_task = cursor.fetchone()

    if deleted_task is None:
        cursor.close()
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    connection.commit()

    cursor.close()
    connection.close()

    return deleted_task