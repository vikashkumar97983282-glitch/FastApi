from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def message():
    return {"message":"hello from fastapi"}


@app.get("/costumer")
def costumer(costumer_id:int):
    return {
        'costumer_id': costumer_id,
        "costumer_name": "Rahul Kumar",
        "costumer_email": "rahulkumar@gmail.com"
    }

# class Student(BaseModel):
#     name: str
#     roll_no: int
#     enrollment_no: str
#     course_name: str
#     college_name: str
#     cgpa: float
#     apptitude_score: float

# @app.post("/student")
# def student(student: Student):

#     if student.cgpa < 7.0:
#         message = "he is not eligible for placement"
#     else:
#         message = "he is eligible for placement"

#     return {
#         "name": student.name,
#         "roll_no": student.roll_no,
#         "enrollment_no": student.enrollment_no,
#         "course_name": student.course_name,
#         "college_name": student.college_name,
#         "cgpa": student.cgpa,
#         "apptitude_score": student.apptitude_score,
#         "message": message
#     }



students = {
    101: {"name": "Rahul Kumar","roll_no": 101,"enrollment_no": "ENR001","course_name": "B.Tech",
        "college_name": "ABC College","cgpa": 8.5,"apptitude_score": 85.0
    },
    102: {"name": "gaurav Kumar","roll_no": 101,"enrollment_no": "ENR001","course_name": "B.Tech",
        "college_name": "ABC College","cgpa": 8.5,"apptitude_score": 85.0
    },
    103: {"name": "vivek Kumar","roll_no": 101,"enrollment_no": "ENR001","course_name": "B.Tech",
        "college_name": "ABC College","cgpa": 8.5,"apptitude_score": 85.0
    },
    104: {"name": "abhishek Kumar","roll_no": 101,"enrollment_no": "ENR001","course_name": "B.Tech",
        "college_name": "ABC College","cgpa": 8.5,"apptitude_score": 85.0
    },
    105: {"name": "raju Kumar","roll_no": 101,"enrollment_no": "ENR001","course_name": "B.Tech",
        "college_name": "ABC College","cgpa": 8.5,"apptitude_score": 85.0
    }
}


@app.post("/students_info/{student_id}")
def get_student(student_id: int):

    if student_id not in students:
        return {"message": f"student {student_id} not found"}
    
    student = students[student_id]

    return {
        "student_id": student_id,
        "name": student["name"],
        "roll_no": student["roll_no"],
        "enrollment_no": student["enrollment_no"],
        "course_name": student["course_name"],
        "college_name": student["college_name"],
        "cgpa": student["cgpa"],
        "apptitude_score": student["apptitude_score"]
    }