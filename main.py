from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from inference import HousePricePredictor
import uvicorn
import os

app = FastAPI(title="California House Price Predictor API")

# Initialize predictor
predictor = HousePricePredictor()
predictor.load()

class HouseData(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: float
    total_rooms: float
    total_bedrooms: float
    population: float
    households: float
    median_income: float
    ocean_proximity: str

@app.post("/predict")
async def predict(data: HouseData):
    try:
        prediction = predictor.predict_single(
            longitude=data.longitude,
            latitude=data.latitude,
            housing_median_age=data.housing_median_age,
            total_rooms=data.total_rooms,
            total_bedrooms=data.total_bedrooms,
            population=data.population,
            households=data.households,
            median_income=data.median_income,
            ocean_proximity=data.ocean_proximity
        )
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
