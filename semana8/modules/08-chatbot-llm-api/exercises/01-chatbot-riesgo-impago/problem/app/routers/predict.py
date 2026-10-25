from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse 
from pydantic import ValidationError

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

router = APIRouter()


# POST /predict (entrada PrestamoEntrada, salida PrediccionSalida)
@router.post("/predict")
def predict(request: dict):
    try:
        pe = PrestamoEntrada(**request)
        ps = predecir(pe)
        return ps.as_dict()
    except ValidationError as e:
        return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": e})
    )
