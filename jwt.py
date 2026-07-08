from fastapi import FastAPI, Depends, HTTPException, Header
#javascript object signing and encryption -- jose
from jose import jwt

from datetime import datetime, timedelta, timezone

app = FastAPI()

SECRET_KEY = "mysecretkey"

ALGORITHM = "HS256"

def create_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return token

@app.post('/login')
def login(username:str, password:str):
    if username != "admin" and password != "password":
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_token({"sub": username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def verify_token(token:str = Header(None)):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    

# protected route
@app.get("/secure")
def secure_data(user = Depends(verify_token)):
    return {
        "message":"secure data accessed",
        "user":user
    }