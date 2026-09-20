from pydantic import BaseModel, Field
from typing import Optional

class TodoPydantic(BaseModel):
    id : int
    title : str = Field(max_length=40)
    description : str = Field(max_length=200)
    priority : int = Field(ge=0, le=5)
    completed : bool
    
class TodoPydanticUpdate(BaseModel):
    title : Optional[str] = Field(default=None, max_length=40)
    description : Optional[str] = Field(default=None, max_length=200)
    priority : Optional[int] = Field(default=None, ge=0, le=5)
    completed : Optional[bool] = Field(default=None)