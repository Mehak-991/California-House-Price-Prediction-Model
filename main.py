import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from inference import HousePricePredictor
import uvicorn
import os
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("house_price_predictor")

app = FastAPI(title="California House Price Predictor API")

logger.info("Initializing HousePricePredictor...")
predictor = HousePricePredictor()
try:
    predictor.load()
    logger.info("Predictor loaded successfully.")
except Exception as e:
    logger.critical(f"Failed to load predictor: {e}", exc_info=True)

class HouseData(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: int
    total_rooms: int
    total_bedrooms: int
    population: int
    households: int
    median_income: float
    ocean_proximity: str

@app.post("/predict")
async def predict(request: Request):
    try:
        # 1. Incoming JSON
        body_bytes = await request.body()
        raw_json = body_bytes.decode("utf-8")
        logger.info(f"Incoming JSON: {raw_json}")

        # 2. Parsed data (Pydantic validation)
        data = HouseData.model_validate_json(raw_json)
        logger.info(f"Parsed data: {data}")

        # 3. DataFrame before prediction
        df = pd.DataFrame([data.model_dump()])
        logger.info(f"DataFrame before prediction:\n{df.to_string(index=False)}")

        # Run prediction
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

        # 4. Prediction result
        logger.info(f"Prediction result: {prediction}")
        return {"prediction": prediction}

    except Exception as e:
        # 5. Complete traceback if exception occurs
        logger.error(f"Prediction failed: {e}", exc_info=True)
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

# Serve static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
