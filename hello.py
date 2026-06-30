from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def message():
    return {"message":"hello from fastapi"}