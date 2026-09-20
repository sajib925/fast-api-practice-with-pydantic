from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from database import SessionLocal
from router.auth import get_current_user
from models import Todo
from fastapi.responses import JSONResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/admin/todos")
def read_all_by_admin(user: user_dependency, db: db_dependency):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="your are not authenticated")
    return db.query(Todo).all()

@router.delete("/admin/delete/{todo_id}")
def delete_todos_by_admin(user: user_dependency, db: db_dependency, todo_id: int):
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=401, detail="your are not authenticated")

    todo = db.query(Todo).filter(Todo.owner_id == user.get('id')).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todo).filter(Todo.id == todo_id).delete()

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'todos deleted successfully'})