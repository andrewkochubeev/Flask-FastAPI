from enum import Enum
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []


class Status(Enum):
    status_1 = 'выполнена'
    status_2 = 'не выполнена'


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: Status


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/tasks")
async def get_tasks():
    return {'tasks': tasks}


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    return {"message": f'Task {task_id} not found'}


@app.post("/tasks")
async def add_task(task: Task):
    tasks.append(task)
    return {'tasks': tasks}


@app.put("/tasks/{task_id}")
async def update_task_by_id(task_id: int, new_task: Task):
    for task in tasks:
        if task.id == task_id:
            task.id = new_task.id
            task.title = new_task.title
            task.description = new_task.description
            task.status = new_task.status
            return {"message": f'Task {task_id} was updated', 'task': task}
    return {"message": f'Task {task_id} not found'}


@app.delete("/tasks/{task_id}")
async def delete_task_by_id(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": f'Task {task_id} was deleted', 'tasks': tasks}
    return {"message": f'Task {task_id} not found'}


if __name__ == '__main__':
    uvicorn.run('hmwrk05:app', reload=True)
