from fastapi import FastAPI, Path, HTTPException, Query, Body
import json
from students_pydantic import Students, StudentUpdate
from fastapi.responses import JSONResponse

app = FastAPI()


def load_data():
    with open('students.json', 'r') as f:
        data = json.load(f)
    return data
def save_data(data):
    with open('students.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def welcome():
    return "Hello! From students management Api"

@app.get("/student/{student_id}")
def view_student(student_id:str = Path(..., description="This is id of student", example="S001")):
    data = load_data()
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404,detail="Students Not Found")
    
@app.get("/students")
def view_student(sorted_by:str = Query(..., description="Sort on the bassis of student_class age."), order: str = Query('asc', description="choose order asc by des")):

    valid_fields = [ "age", "student_class", "roll", "Math_marks", "English_marks", "Science_marks",]

    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404,detail=f"Invalid Field selected by {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=404,detail=f"Choose between asc or desc")
    
    data = load_data()

    if order == 'asc':
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x: x[sorted_by])
        return sorted_data
    else:
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x: x[sorted_by], reverse=True)
        return sorted_data       

@app.post("/create")
def create_student(student:Students):
    data = load_data()

    if student.id in data:
        raise HTTPException(status_code=400, detail=f'Student id already exits')
    
    data[student.id] = student.model_dump(exclude=['id'])

    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Successfully Created Student"})

@app.put("/update/{student_id}")
def update_student(student: StudentUpdate, student_id:str):
    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=400, detail=f'Student Not Found')
    
    data[student_id].update(student.model_dump(exclude_unset=True))

    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Successfully Updated Student"})

@app.delete("/update/{student_id}")
def delete_student(student_id:str):
    data = load_data()

    if student_id not in data:
        raise HTTPException(status_code=400, detail=f'Student Not Found')
    
    del data[student_id]

    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Successfully Deleted Student"})

