import joblib

from app.config import MODEL_PATH
from app.schemas.prestamo import PrediccionSalida

# Orden en el que el modelo espera las variables
VARIABLES = [
    "edad",
    "ingresos_mensuales",
    "importe_prestamo",
    "plazo_meses",
    "antiguedad_laboral_anios",
    "impagos_previos",
]

# cargar el modelo joblib una sola vez, al importar el modulo
# funcion decidir(probabilidad) -> "aprobar", "revisar" o "rechazar" (umbrales en el enunciado)
# funcion predecir(entrada) -> PrediccionSalida, usando VARIABLES para ordenar los valores

MODEL = joblib.load(MODEL_PATH)



def decidir(probabilidad):
    if probabilidad < 0.2:
        return "aprobar"
    elif probabilidad < 0.5:
        return "revisar"
    else:
        return "rechazar"

def predecir(entrada):
    v = entrada.to_vector()
    prob_impago = MODEL.predict_proba(v)[0][1]
    prob_str = decidir(prob_impago)
    ps = PrediccionSalida(probabilidad_impago=prob_impago, decision=prob_str)
    return ps