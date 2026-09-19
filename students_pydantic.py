from pydantic import BaseModel, Field
from typing import Annotated, Optional

class Students(BaseModel):
    id: Annotated[str, Field(..., description="Id of the student", examples=["S001"])]
    name: Annotated[str, Field(..., description="Name of the student", examples=["Jhon doe"])]
    age: Annotated[int, Field(..., ge=5, le=40, description="Age of the student (5 to 40)", examples=[6])]
    student_class: Annotated[int, Field(..., ge=1, le=12, description="Class of the student (1 to 12)", examples=[10])]
    roll: Annotated[int, Field(..., ge=1, le=100, description="Roll of the student (1 to 100)", examples=[10])]
    Math_marks: Annotated[int, Field(..., ge=0, le=100, description="Math marks (0 to 100)", examples=[80])]
    English_marks: Annotated[int, Field(..., ge=0, le=100, description="English marks (0 to 100)", examples=[80])]
    Science_marks: Annotated[int, Field(..., ge=0, le=100, description="Science marks (0 to 100)", examples=[80])]
    phone: Annotated[str, Field(..., description="Phone number of the student", examples=["01756906993"])]

class StudentUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    student_class: Annotated[Optional[int], Field(default=None)]
    roll: Annotated[Optional[int], Field(default=None)]
    Math_marks: Annotated[Optional[int], Field(default=None)]
    English_marks: Annotated[Optional[int], Field(default=None)]
    Science_marks: Annotated[Optional[int], Field(default=None)]
    phone:Annotated[Optional[str], Field(default=None)]