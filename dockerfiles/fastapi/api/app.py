from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import mlflow
import os

# --- 1) Configuración MLflow ---
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = "WineSentiment"
MODEL_STAGE = "Production"

# Set the MLflow tracking URI
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# --- 2) Inicializar FastAPI ---
app = FastAPI(
    title="Wine Sentiment API",
    version="1.0.0",
    description="Predice sentimiento (+subjetividad) para reviews de vinos"
)

# --- 3) Cargar modelo desde MLflow ---
model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{MODEL_NAME}/{MODEL_STAGE}"
)

# --- 4) Modelos Pydantic ---
class Review(BaseModel):
    text: str = Field(..., example="Aromas of honey, vanilla and ripe apple…")

class Prediction(BaseModel):
    sentiment: str
    polarity: float
    subjectivity: float

# --- 5) Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Model Service"}

@app.post("/predict/", response_model=Prediction)
def predict(review: Review):
    try:
        preds = model.predict([review.text])[0]
        return Prediction(**preds)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

