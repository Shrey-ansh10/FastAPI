# creating a API to expose the ML model using FastAPI.
# based on the input parameters the model will predict if the insurance price for the specific user will be High, Low or Medium

from fastapi import FastAPI
from .schema.user_input import Input
import logging, traceback
from fastapi.responses import JSONResponse
from .models.predict import predict, _model, MODEL_VERSION

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# creating endpoint to serve request

@app.get("/")
def root():
    return {"message": "Insurance category predictor API"}

# health check endpoint for cloud services
@app.get('/health')
def health_check():
    return {
        "status" : "ok",
        "version" : MODEL_VERSION,
        "model_loaded": _model is not None,
     }


# POST endpoint
@app.post('/predict')
def predict_insurance(data : Input):
    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:
        prediction = predict(user_input)
        return JSONResponse(status_code=200, content=prediction) #changing content here | prev -> {'predited_category' : prediction}
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))