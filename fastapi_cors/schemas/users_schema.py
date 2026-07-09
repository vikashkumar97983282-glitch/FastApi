from pydantic import BaseModel,EmailStr


class userRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class userLogin(BaseModel):
    email: EmailStr
    password: str

class userResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
