"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

import joblib
import os
import numpy as np

# CHANGE TO DEFAULT PATH
DEFAULT_MODEL_PATH = "../../assets/model/wine_quality_classifier.joblib"

def load_wine_quality_model():
    
    if not os.path.exists(DEFAULT_MODEL_PATH):
        raise Exception("[X] ERROR: Unable to load model. Check path")
    model = joblib.load(DEFAULT_MODEL_PATH)
    return model



def infer_wine_quality(data: list, model):
    arr = np.array(data)
    d = arr.reshape(1, -1)
    p = model["estimator"].predict(d)[0]
    c = max (model["estimator"].predict_proba(d)[0])
    return p, c