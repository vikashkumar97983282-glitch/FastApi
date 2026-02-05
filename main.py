from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message":"hello vikash"}

@app.get("/about")
def about():
    return {"message":"this is about page of fastapi"}