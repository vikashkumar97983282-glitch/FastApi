from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

## local module
from schemas.users_schema import userRegister,userLogin,userResponse

from core.database import user_collection


app = FastAPI()


# allow origins 
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)




@app.get("/")
def home():
    return {
        "message":"cors enable api.",
        "status":"Running....."
    }


@app.get("/about", response_model=list[userResponse])
async def about():

    users = await user_collection.find().to_list(length=None)

    if not users:
        raise HTTPException(
            status_code=400,
            detail="on users available"
        )

    result = []

    for user in users:
        result.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        })

    return result


@app.post("/login")
async def login(user : userLogin):

    existing_user = await user_collection.find_one({"email":user.email, "password":user.password})
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail= "Unauthorized. Access denied!.",
        )
    
    existing_user["_id"] = str(existing_user["_id"])

    return {
        "message":"login successfull",
        "data": existing_user
    }

@app.post("/register")
async def register(user: userRegister):

    existing_user = await user_collection.find_one({"email":user.email})

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email Already exists"
        )
    
    new_user = {
        "name":user.name,
        "email":user.email,
        "password":user.password
    }
    
    data = await user_collection.insert_one(new_user)

    return {
        "id": str(data.inserted_id),
        "message":"user register successfully"
    }