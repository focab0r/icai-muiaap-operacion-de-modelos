from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse 

from app.schemas.chat import ChatEntrada, ChatSalida, Mensaje
from app.services.llm import get_llm
from app.services.orquestador import responder

router = APIRouter()


# POST /chat (entrada ChatEntrada, salida ChatSalida). Recibe el LLM con Depends(get_llm)
@router.post("/chat")
def chat(request: dict, llm = Depends(get_llm)):
    m_list = []
    try:
        for elem in request["mensajes"]:
            m_list.append(Mensaje(role=elem["role"], content=elem["content"]))
        cs = responder(m_list, llm)
        return {"respuesta": cs.respuesta, "herramienta": cs.herramienta}
    except Exception as e:
        return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": e})
    )