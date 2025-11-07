# creating a endpoint to expose the ML model using FastAPI
# based on the input parameters the model will predict if the insurance price for the specific user will be High, Low or Medium


from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Annotated
import pickle
from pathlib import Path
import pandas as pd
import logging, traceback
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# defer pandas import until needed so we can catch ImportError clearly
# pd = None

# loading the ml model lazily and robustly
MODEL_PATH = Path(__file__).parent / "model.pkl"
_model = None

def load_model():
    global _model
    if _model is not None:
        return _model
    try:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        if not hasattr(_model, "predict"):
            raise RuntimeError("Loaded object does not expose a 'predict' method")
        logger.info("Model loaded successfully from %s", MODEL_PATH)
        return _model
    except Exception as e:
        logger.exception("Error loading model: %s", e)
        # Re-raise so callers can decide how to handle it (or return 500)
        raise

# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

app = FastAPI()

# tier of cities   
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
"Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
"Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
"Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
"Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
"Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
"Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


#pydantic model to validate incoming data from client
class Input(BaseModel):
    age: Annotated[int, Field(..., gt=16, lt=100, description="age of user")]
    weight: Annotated[float, Field(..., gt=30, lt=300, description="enter the weight")]
    height: Annotated[float, Field(..., gt=0, lt=3, description="give height in meters")]
    income_lpa: Annotated[float, Field(..., description="Income of user in lacks per annum")]
    smoker: Annotated[bool, Field(..., description="true or false")]
    city: Annotated[str, Field(..., description="city in which the user lives")]
    occupation: Annotated[Literal['student', 'retired', 'freelancer', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description="occupation of the user")]

    # Following are the features derived from the input featues. 
    # The model accepts only these and hence we will need to calculate them.

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi >30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        if self.age < 45:
            return "adult"
        if self.age < 65:
            return "middle_aged"
        else:
            return "senior"

    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


# creating endpoint to serve request

# @app.get("/")
# def root():
#     return {"message": "Insurance category predictor API"}

# POST

@app.post('/predict')
def predict(data : Input):

        # load model (lazy)
    try:
        model = load_model()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "model load failed",
                "detail": str(e),
                "trace": traceback.format_exc()
            }
        )
 

    # build input DataFrame and predict
    try:
        input_data = pd.DataFrame([{
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }])
    except Exception as e:
        logger.exception("Failed building input DataFrame: %s", e)
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to build input DataFrame",
                "detail": str(e),
                "trace": traceback.format_exc()
            }
        )

    # run prediction
    try:
        prediction = model.predict(input_data)[0]
    except Exception as e:
        logger.exception("Model prediction failed: %s", e)
        return JSONResponse(
            status_code=500,
            content={
                "error": "model prediction failed",
                "detail": str(e),
                "trace": traceback.format_exc()
            }
        )

    return JSONResponse(status_code=200, content={'predited_category' : prediction})