from fastapi import FastAPI
from database import get_connection

app = FastAPI()


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