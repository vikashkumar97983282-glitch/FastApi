import io

import pandas as pd
import joblib

from fastapi import FastAPI ,HTTPException,UploadFile,File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field


app = FastAPI()


model = joblib.load("house_model.joblib")
features = joblib.load("features_columns.joblib")
scaler = joblib.load("scaler.joblib")


@app.get("/")
def home():
    return {"message": "Welcome to the House Price Prediction API!"}


# MedInc	HouseAge	AveRooms	AveBedrms	Population	AveOccup	Latitude	Longitude	Price
class HouseData(BaseModel):
    MedInc: float = Field(..., description="Median income in block group")
    HouseAge: float = Field(..., description="Median house age in block group")
    AveRooms: float = Field(..., description="Average number of rooms per household")
    AveBedrms: float = Field(..., description="Average number of bedrooms per household")
    Population: float = Field(..., description="Block group population")
    AveOccup: float = Field(..., description="Average number of household members")
    Latitude: float = Field(..., description="Block group latitude")
    Longitude: float = Field(..., description="Block group longitude")

@app.post("/predict")
def predict_price(data: HouseData):
    try:
        # Convert the input data to a DataFrame
        input_data = pd.DataFrame([data.dict()])

        # Ensure the input data has the same columns as the model's features
        input_data = input_data[features]

        # Scale the input data
        scaled_data = scaler.transform(input_data)

        # Make prediction
        prediction = model.predict(scaled_data)

        return {"predicted_price": float(prediction[0]*100000)+24031.0+32754.0}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@app.post("/predict_file")
async def predict_file(file: UploadFile = File(...)):
    