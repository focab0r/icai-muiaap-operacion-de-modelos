import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir

NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)

RISK_TOOL = {
    "id": "call_1",
    "type": "function",
    "function": {"name": NOMBRE_TOOL},
}


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


# definir_tool() -> dict con la definicion de la tool, sacando "parameters" de PrestamoEntrada
def definir_tool():
    d = {}
    d["type"] = "function"
    d["function"] = {}
    d["function"]["name"] = NOMBRE_TOOL
    d["function"]["parameters"] = {}
    d["function"]["parameters"]["properties"] = PrestamoEntrada.model_fields
    return d
         
    
# ejecutar_tool(nombre, argumentos_json) -> dict con "ok" True/False
#       (tool desconocida, JSON roto, datos invalidos o campos inventados -> ok False con el error)
def ejecutar_tool(nombre, argumentos_json):
    data = leer_argumentos(argumentos_json)
    if data == {}:
        return {"ok": False, "error": "Unable to decode JSON"}
    if nombre != NOMBRE_TOOL:
        return {"ok": False, "error": "Invalid tool selected"}
    try:
        pe = PrestamoEntrada(**data)
        ps = predecir(pe).as_dict()
        ps["ok"] = True
        return ps
    except Exception as e:
        return {"ok": False, "error": f"Error when creating contract: {e}"}


# responder(mensajes, llm) -> ChatSalida, con el bucle LLM -> tool -> LLM (maximo MAX_VUELTAS)
def responder(mensajes, llm):
    
    vuelta = 0
    herramienta_usada = None
    messages_history = [{"role": "system"}]
    messages_history.append({"role": mensajes[0].role, "content": mensajes[0].content})
    while (vuelta <= MAX_VUELTAS):
        vuelta += 1
        response = llm.completar(messages_history, [RISK_TOOL])
        messages_history.append(response)
        if response["content"] != None:
            return ChatSalida(respuesta=response["content"], herramienta=herramienta_usada)
        else:
            tool = response["tool_calls"][0]["function"]["name"]
            argumentos_json = response["tool_calls"][0]["function"]["arguments"]
            resultado = ejecutar_tool(tool, argumentos_json)
            messages_history.append({"role": "tool", "content": resultado})
            herramienta_usada = HerramientaUsada(nombre=tool, argumentos=leer_argumentos(argumentos_json), resultado=resultado)

    return ChatSalida(respuesta="ERROR: too much recursion")