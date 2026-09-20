from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic_todos import UserPydantic
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime, timezone
from jose import jwt

router = APIRouter()
SECRETE_KEY='542b87fe8b0c9225c6aa6116d1a736c9d69bc8704923564bd147d51beca23306'
ALGRORITHOM='HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='login-user')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username, password, db):
    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        return False

    if bcrypt_context.verify(password, user.hash_password):
        return user
    else:
        return

def create_access_token(username, user_id, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'role': role, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    token = jwt.encode(encode, SECRETE_KEY, algorithm=ALGRORITHOM )
    return {'access_token': token, 'token_type': 'bearer'}

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGRORITHOM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role : str = payload.get('role')

        if username is None:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return {'username': username, 'role': role, 'id': user_id}

    except:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/create-user")
def create_user(db: db_dependency, new_user: UserPydantic):
    user_model = Users(
        username = new_user.username,
        email = new_user.email,
        firstname = new_user.firstname,
        lastname = new_user.lastname,
        hash_password = bcrypt_context.hash(new_user.password),
        is_active = True,
        role = new_user.role
    )

    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=201, content={'message': 'user created successfully'})

@router.post("/login-user")
def login_user(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        return "Failed Authentication"
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))
    return token
    

