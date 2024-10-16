from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from pydantic import BaseModel
import util

@asynccontextmanager
async def lifespan(app: FastAPI):
    # # This block runs when the server starts or reloads
    # print("Server is starting or reloading...")
    util.load_saved_artifacts()
    
    yield  # After this point, the app will start serving requests

    # This block runs when the server shuts down
    # print("Server is shutting down...")

# Create the FastAPI app and pass the lifespan context
app = FastAPI(lifespan=lifespan)


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/get_location_names")
async def get_location_names():
    return {"locations": util.get_location_names()}

@app.get("/get_area_types")
async def get_area_types():
    return {"area_type": util.get_area_types()}

@app.get("/get_areas_and_locations")
async def get_area_types():
    return {"area_type": util.get_area_types(),"locations": util.get_location_names()}

class PricePredictionRequest(BaseModel):
    location: str
    area_type: str
    total_sqft: float
    bhk: int
    bath: int
    balcony:int

@app.post("/predict_home_price")
async def predict_home_price(
    total_sqft: float = Form(...),
    location: str = Form(...),
    area_type: str =Form(...),
    bhk: int = Form(...),
    bath: int = Form(...),
    balcony:int = Form(...),
):
    estimated_price = util.get_estimated_price(area_type,location, total_sqft, bhk, bath,balcony)
    return {"estimated_price": estimated_price}

if __name__ == "__main__":
    
    print("Starting FastAPI Server For Home Price Prediction...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
    
