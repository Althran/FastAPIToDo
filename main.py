import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "https://localhost:7098",
    "http://localhost:5012"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

item_dict = {
    0: {
        'name_id': 0,
        'name': 'Sample task',
        'description': 'Sample description',
        'done': False
    },
    1: {
        'name_id': 1,
        'name': 'Sample completed task',
        'description': 'Sample description of completed task',
        'done': True
    },
}
completed_tasks = {}


class Task(BaseModel):
    name: str
    name_id: int
    description: str
    done: bool

    class Config:
        schema_extra = {
            'example': {
                'name': 'Sample_name',
                'name_id': 0,
                'description': 'Some description',
                'done': False,
            }
        }


@app.get('/task/')
def read_all():
    return [*item_dict.values()]


@app.get("/task/{task_id}")
async def read_item(task_id: int):
    if task_id not in item_dict:
        raise HTTPException(status_code=404, detail='task not found')
    return item_dict[task_id]


@app.post('/task/')
def add_item(task: Task):
    next_id = max([*item_dict.keys()]) + 1
    task.name_id = next_id
    item_dict[task.name_id] = task
    return task


@app.delete('/task/{name_id}')
def delete_task(name_id: int):
    if name_id not in item_dict:
        raise HTTPException(status_code=404, detail='task not found')
    del item_dict[name_id]
    return f'{name_id} was deleted'


@app.put('/task/{name_id}')
def update_task(name_id: int, task: Task):
    item_dict[name_id] = task
    return f'{task} was updated'


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=5000)
