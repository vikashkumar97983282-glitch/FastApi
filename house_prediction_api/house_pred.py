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
    return {
        "message": "Welcome to the California_House_Price Prediction API!",
        "status": "API is running.",
        "endpoints 1": "POST ( /predict ) - Predict house price based on single input features.",
        "endpoints 2": "POST ( /predict_file ) - Predict house prices based on a CSV file.",
        "help": "GET ( /help ) - Get information about the API and its endpoints."
    }


@app.get("/help")
def help():
    return {
        "message": "This API predicts California house prices based on input features.",
        "endpoints": {
            "/predict": {
                "method": "POST",
                "description": "Predict house price based on single input features.",
                "input_format": {
                    "MedInc": "float - Median income in block group",
                    "HouseAge": "float - Median house age in block group",
                    "AveRooms": "float - Average number of rooms per household",
                    "AveBedrms": "float - Average number of bedrooms per household",
                    "Population": "float - Block group population",
                    "AveOccup": "float - Average number of household members",
                    "Latitude": "float - Block group latitude",
                    "Longitude": "float - Block group longitude"
                },
                "output_format": {
                    "predicted_price": "float - Predicted house price"
                }
            },
            "/predict_file": {
                "method": "POST",
                "description": "Predict house prices based on a CSV file.",
                "input_format": {
                    "file": ".csv file containing the required columns"
                },
                "output_format": {
                    ".csv file with an additional column 'predicted_columns' containing predicted prices"
                }
            }
        }
    }

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
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    contents = await file.read()

    df = pd.read_csv(io.BytesIO(contents))

    required_columns = ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"]

    missing_columns = {
        col for col in required_columns
        if col not in df.columns
    }

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_columns)}"
        )

    if len(df) == 0:
        raise HTTPException(
            status_code=400,
            detail="The uploaded CSV file is empty."
        )
    
    try:
        x = df[required_columns]
        X_scaled = scaler.transform(x)

        predictions = model.predict(X_scaled)

        predictions = [float(pred*100000)+24031.0+32754.0 for pred in predictions]

        df["predicted_columns"] = predictions

        df['predicted_columns'] = df['predicted_columns'].apply(lambda x: f"${x:,.0f}")

        output = df.to_csv(index=False)

        return StreamingResponse(
            io.StringIO(output),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=predictions.csv"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"something went wrong: {str(e)}")