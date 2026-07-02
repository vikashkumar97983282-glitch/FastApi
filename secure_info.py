from fastapi import FastAPI
from pydantic import BaseModel,Field


app = FastAPI()


class User(BaseModel):
    username: str = Field(min_length=8, max_length=12)
    password: str = Field(min_length=8, max_length=12)
    name: str
    age: int

class SecureInfo(BaseModel):
    username: str
    name: str
    age: int

users_db = []


# home route
@app.get("/")
def home():
    return {"message": "Welcome to the secure info API!"}

# get all users route
@app.get("/users", response_model=list[SecureInfo])
def get_users():

    return users_db


@app.post("/users")
def create_user(user: User):

    if user.name.strip() == "":
        return {"error": "Please field name is required."}
    
    if user.age < 15 or user.age > 60:
        return {"error": "Age must be between 15 and 60."}
    
    try:

        users_db.append(user)
        return {"message": "user created sucessfully!"}
    
    except Exception as e:
        return {"error": f"Internal server errror {str(e)}"}
