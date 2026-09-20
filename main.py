from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todo
import models
from database import engine, SessionLocal
from pydantic_todos import TodoPydantic, TodoPydanticUpdate
from fastapi.responses import JSONResponse


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/todos")
def read_todos(db: db_dependency):
    return db.query(Todo).all()

@app.get("/todo/{todo_id}")
def read_todos(db: db_dependency, todo_id: int):

    specific_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if specific_todo is not None:
        return specific_todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/create")
def write_totdos(db: db_dependency, new_todo: TodoPydantic):
    todo_model = Todo(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()
    return JSONResponse(status_code=201, content={'message': 'todo created successfully'})
    
@app.put("/edit/{todo_id}")
def read_todos(db: db_dependency, todo_id: int, update_todo: TodoPydanticUpdate):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = update_todo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'todos updated successfully'})
@app.delete("/edit/{todo_id}")
def read_todos(db: db_dependency, todo_id: int):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todo).filter(Todo.id == todo_id).delete()

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'todos deleted successfully'})