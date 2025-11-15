import pickle
from pathlib import Path
import logging, traceback
from ..schema import Input
import pandas as pd
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# loading the ml model lazily and robustly
MODEL_PATH = Path(__file__).parent / "model.pkl"
_model = None

MODEL_VERSION = 1.0

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

# prediction function
def predict(data : dict):

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

    #extracting all class lables from the model - possible category of output
    class_lables = model.classes_.tolist()

    # build input DataFrame and predict
    try:
        input_data = pd.DataFrame([data])
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
        # predicting using model
        prediction = model.predict(input_data)[0]

        # also collecting probabilities for all output classes
        probabilities = model.predict_proba(input_data)[0]
        confidence = max(probabilities) # confidence in the predicted output

        #create mapping for probabilites of all classes -> {class : probability}
        class_probs = dict(zip(class_lables, map(lambda p: round(p,4), probabilities)))

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

    return {
        "predicted_category" : prediction,
        "confidence" : round(confidence, 4),
        "class_probabilities" : class_probs #this will be a dictionary in itself
    }