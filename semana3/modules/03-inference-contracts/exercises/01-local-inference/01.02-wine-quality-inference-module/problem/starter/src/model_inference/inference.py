"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.

import joblib
import os
import numpy as np
import sys

from model_inference.preprocess import FEATURE_NAMES

# CHANGE TO DEFAULT PATH
DEFAULT_MODEL_PATH = "../../assets/model/wine_quality_classifier.joblib"

def load_wine_quality_model(path):
    
    if not os.path.exists(path):
        raise Exception("[X] ERROR: Unable to load model. Check path")
    model = joblib.load(path)
    if "estimator" not in model.keys():
        sys.stderr.write(f'[X] ERROR: Null estimator detected in the model: [clasificador compatible]')
        sys.exit(2)     
    if model["feature_names"] != list(FEATURE_NAMES):
        sys.stderr.write(f'[X] ERROR: Invalid feature_names detected in the model')
        sys.exit(2)
    if model["estimator"].constant == 'unknown':
        sys.stderr.write(f'[X] ERROR: Invalid estimator: [quality_band]')
        sys.exit(2)
    return model



def infer_wine_quality(data: list, model):
    arr = np.array(data)
    d = arr.reshape(1, -1)
    p = model["estimator"].predict(d)[0]
    c = max (model["estimator"].predict_proba(d)[0])
    return p, c