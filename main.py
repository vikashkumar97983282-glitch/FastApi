from fastapi import FastAPI, Path
import json

app = FastAPI()


def load_data():
    with open("practical.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/")
def hello():
    return {"message":"hello vikash"}

@app.get("/about")
def about():
    return {"message":"this is about page of fastapi"}


@app.get("/view")
def view():
    data = load_data()
    return data


@app.get("/cust/{cust_id}")
def view_cust(cust_id: str = Path(..., description="ID of the customer to view", example="P001")):

    data = load_data()

    if cust_id in data:
        return data[cust_id]
    return {"message": "data not found"}