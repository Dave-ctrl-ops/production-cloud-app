from fastapi import FastAPI
from pydantic import BaseModel
from database import get_connection

app = FastAPI()


class Task(BaseModel):
    title: str
    description: str


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