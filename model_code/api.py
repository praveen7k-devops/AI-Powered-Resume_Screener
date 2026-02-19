# -*- coding: utf-8 -*-

import pandas as pd
from pycaret.classification import load_model, predict_model
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import json

# Create the app
app = FastAPI()

# Configure CORS (allow all origins for development; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained Pipeline
model = load_model("ai_resume_screener_model")

# Create input/output pydantic models
# Use explicit BaseModel classes instead of create_model to avoid pydantic-core schema generation errors
class InputModel(BaseModel):
    years_experience: int = 5
    skills_match_score: float = 66.4000015258789
    education_level: str = "Masters"
    project_count: int = 7
    resume_length: int = 595
    github_activity: int = 320

class NameModel(BaseModel):
    name: str = "test_candidate"

class OutputModel(BaseModel):
    name: str = "test_candidate"
    factors: InputModel = {}
    prediction: int = 1

# Define predict function
@app.post("/predict-model", response_model=OutputModel)
def predict_model_endpoint(data: InputModel):
    df = pd.DataFrame([data.dict()])
    predictions = predict_model(model, data=df)
    return {"prediction": predictions["prediction_label"].iloc[0]}

@app.post("/predict", response_model=OutputModel)
def predict_by_name(name_model: NameModel):
    # Load JSON file as a dict and construct a one-row DataFrame for the named candidate
    try:
        with open('test_dict.json', 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="test_dict.json not found on server")
    if name_model.name not in json_data:
        raise HTTPException(status_code=404, detail=f"Name '{name_model.name}' not found in data")

    row = json_data[name_model.name]
    # Ensure we create a DataFrame with a single row matching the model's expected features
    print(row)
    print(row['years_experience'])
    df = pd.DataFrame([row])
    print(df)
    predictions = predict_model(model, data=df)
    return {
        "name": name_model.name,
        "prediction": predictions["prediction_label"].iloc[0],
        "factors": {
            "years_experience": row['years_experience'],
            "skills_match_score": row['skills_match_score'],
            "education_level": row['education_level'],
            "project_count": row['project_count'],
            "resume_length": row['resume_length'],
            "github_activity": row['github_activity'],
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
