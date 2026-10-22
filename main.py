from fastapi import FastAPI,HTTPException
from pathlib import Path
import json
from pydantic import BaseModel


DATA = Path(__file__).parent / 'todos.json'
def load_todos():
    if not DATA.exists():
        return []
    try:
        return json.loads(DATA.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        print('文件已损坏，已重置为空列表')
        return []

def save_todos(todos):
    DATA.write_text(json.dumps(todos,ensure_ascii= False),
                    encoding = 'utf-8')

class Todoin(BaseModel):
    task : str

class TodoUpdate(BaseModel):
    task : str | None = None
    done : bool | None = None

app = FastAPI()

@app.get("/")
def home():
    return {'name':'todo','status':'running'}

@app.get("/todos")
def list_todos():
    return load_todos()

@app.get("/todos/{todo_id}")
def one_todos(todo_id:int):
    todos = load_todos()

    for t in todos:
        if t['id'] == todo_id:
            return t
    raise HTTPException(status_code=404,detail='没有这条待办')


@app.post('/todos')
def add_todos(todo:Todoin):
    todos = load_todos()
    new_id = max((t['id'] for t in todos),default=0) + 1
    new_todo = {'id':new_id,'task':todo.task,'done':False}
    todos.append(new_todo)
    save_todos(todos)
    return new_todo

@app.delete("/todos/{todo_id}")
def delete_todos(todo_id:int):
    todos = load_todos()
    
    for i,t in enumerate(todos):
        if t['id'] == todo_id:
            todos.pop(i)
            save_todos(todos)
            return {"message":"删除成功"}
            
    
    raise HTTPException(status_code=404, detail="没有这条待办")

@app.patch('/todos/{todo_id}')
def update_todos(todo_id : int,payload : TodoUpdate):
    todos = load_todos()

    for t in todos:
        if t['id'] == todo_id:
            if payload.task is not None:
                t['task'] = payload.task
            if payload.done is not None:
                t['done'] = payload.done

            save_todos(todos)
            return t
    raise HTTPException(status_code=404,detail="没有这条待办")
        