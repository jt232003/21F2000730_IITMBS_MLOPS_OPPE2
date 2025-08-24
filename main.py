import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Create a FastAPI app instance
app = FastAPI(title="Heart Disease Prediction API")

# 2. Define the data input format using Pydantic
# This ensures that the API receives data in the correct format.
class HeartDiseaseInput(BaseModel):
    age: int
    gender: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int

# 3. Load the trained model
# This model is loaded once when the API starts.
model = joblib.load('model.joblib')

# 4. Create the prediction endpoint
@app.post("/predict")
def predict(data: HeartDiseaseInput):
    """
    Receives patient data and returns a heart disease prediction.
    """
    # Convert the input data into a pandas DataFrame
    # The model expects a 2D array, so we create a DataFrame with a single row.
    input_df = pd.DataFrame([data.dict()])

    # Make a prediction
    prediction = model.predict(input_f)
    
    # Get the probability of the prediction
    # predict_proba returns probabilities for [class_0, class_1]
    probability = model.predict_proba(input_df)[0][1]

    # Return the prediction and its probability
    return {
        "prediction": int(prediction[0]),
        "probability_of_heart_disease": float(probability)
    }