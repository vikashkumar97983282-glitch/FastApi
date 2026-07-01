from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


students = [
    {"id": "S001", "name": "Rahul Kumar", "roll_no": 101, "enrollment_no": "ENR001", "course_name": "B.Tech"},
    {"id": "S002", "name": "Gaurav", "roll_no": 102, "enrollment_no": "ENR002", "course_name": "M.Tech"},
    {"id": "S003", "name": "Rahul Yadav", "roll_no": 103, "enrollment_no": "ENR003", "course_name": "BCA"},
    {"id": "S004", "name": "Shivesh Singh", "roll_no": 104, "enrollment_no": "ENR004", "course_name": "MCA"},
    {"id": "S005", "name": "Raju Mandal", "roll_no": 105, "enrollment_no": "ENR005", "course_name": "Diploma"},
    {"id": "S006", "name": "Ram Prakash Kurmi", "roll_no": 106, "enrollment_no": "ENR006", "course_name": "Pharmacy"},
    {"id": "S007", "name": "Abhishek Kisko", "roll_no": 107, "enrollment_no": "ENR007", "course_name": "MBBS"},
]


class student_info(BaseModel):
    id: str
    name: str
    roll_no: int
    enrollment_no: str
    course_name: str



@app.get("/")
def home():
    return {"message": "hello from fastapi"}


@app.get("/get_students/{student_id}")
def get_students(student_id: str):

    all_students =[s for s in students if s["id"] == student_id]

    
    if not all_students:
        raise HTTPException(
            status_code=404,
            detail="student not found"
        )     
        
    return all_students


@app.post("/add_student")
def add_student(student: student_info):

    if student.roll_no < 100 or student.roll_no > 999:
        raise HTTPException(
            status_code=400,
            detail="roll number must be between 100 and 999"
        )


    if student.id.strip() == "" or student.name.strip() == "" or student.enrollment_no.strip() == "" or student.course_name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="id, name, enrollment_no, and course_name cannot be empty"
        )

    try:
        new_student = [] 
        new_student.append(student)
        return {"message": "student added successfully", "student": new_student}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error: " + str(e)
        )

