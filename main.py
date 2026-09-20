from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todo
import models
from database import engine, SessionLocal
from pydantic_todos import TodoPydantic, TodoPydanticUpdate
from fastapi.responses import JSONResponse
from router import auth, admin
from router.auth import get_current_user


app = FastAPI()

models.Base.metadata.create_all(engine)

# connect with others api routes
app.include_router(auth.router)
app.include_router(admin.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/todos")
def read_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="your are not authenticated")
    return db.query(Todo).filter(Todo.owner_id == user.get('id')).all()

@app.get("/todo/{todo_id}")
def read_todos(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="your are not authenticated")

    specific_todo = db.query(Todo).filter(Todo.owner_id == user.get('id')).filter(Todo.id == todo_id).first()
    
    if specific_todo is not None:
        return specific_todo
    else:
        raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/create")
def write_totdos(user: user_dependency, db: db_dependency, new_todo: TodoPydantic):
    if user is None:
        raise HTTPException(status_code=401, detail="your are not authenticated")
    todo_model = Todo(**new_todo.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    return JSONResponse(status_code=201, content={'message': 'todo created successfully'})
    
@app.put("/edit/{todo_id}")
def read_todos(user: user_dependency, db: db_dependency, todo_id: int, update_todo: TodoPydanticUpdate):
    if user is None:
            raise HTTPException(status_code=401, detail="your are not authenticated")

    todo = db.query(Todo).filter(Todo.owner_id == user.get('id')).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    update_data = update_todo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'todos updated successfully'})
@app.delete("/delete/{todo_id}")
def delete_todos(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="your are not authenticated")

    todo = db.query(Todo).filter(Todo.owner_id == user.get('id')).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todo).filter(Todo.owner_id == user.get('id')).filter(Todo.id == todo_id).delete()

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'todos deleted successfully'})