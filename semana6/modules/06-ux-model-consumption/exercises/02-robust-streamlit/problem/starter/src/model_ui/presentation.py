"""TODOs de la vista UX: copy de salida y traducción de errores."""

from __future__ import annotations

from model_ui.errors import ArtifactUnavailableError, InputContractError, InferenceTimeoutError, BackendInferenceError

from model_ui.contracts import PredictionPayload, PredictionView, UserFacingError
from model_ui.policies import (
    DEFAULT_CONFIDENCE_POLICY,
    DEFAULT_LATENCY_POLICY,
    ConfidencePolicy,
    LatencyPolicy,
    classify_confidence,
    classify_latency
)

QUALITY_LABELS = {
    "needs_review": "Requiere revisión",
    "acceptable": "Resultado aceptable",
    "excellent": "Resultado excelente",
}

CONFIDENCE_COPY = {
    "low": (
        "Confianza baja",
        "El resultado es orientativo y requiere revisión; "
        "la confianza no es una garantía.",
    ),
    "medium": (
        "Confianza intermedia",
        "Usa el resultado como señal orientativa y revisa su contexto antes de actuar.",
    ),
    "high": (
        "Confianza alta",
        "La confianza es alta para este modelo, pero no garantiza "
        "que la decisión sea correcta.",
    ),
}

LATENCY_COPY = {
    "within_target": (
        "Dentro del objetivo",
        "La respuesta quedó dentro del objetivo de la demo.",
    ),
    "above_target": (
        "Por encima del objetivo",
        "La respuesta llegó, pero la latencia supera el objetivo técnico de la demo.",
    ),
}


def build_prediction_view(
    prediction: PredictionPayload,
    latency_ms: float,
    *,
    confidence_policy: ConfidencePolicy = DEFAULT_CONFIDENCE_POLICY,
    latency_policy: LatencyPolicy = DEFAULT_LATENCY_POLICY,
) -> PredictionView:
    """construye la vista con etiquetas, confianza, latencia y versiones."""

    confidence_level = classify_confidence(prediction.confidence)
    latency_status = classify_latency(latency_ms)

    return PredictionView(
        quality_band=prediction.quality_band,
        quality_label=QUALITY_LABELS[prediction.quality_band],
        confidence=prediction.confidence,
        confidence_level=confidence_level,
        confidence_label=CONFIDENCE_COPY[confidence_level][0],
        confidence_message=CONFIDENCE_COPY[confidence_level][1],
        latency_ms=latency_ms,
        latency_status=latency_status,
        latency_label=LATENCY_COPY[latency_status][0],
        latency_message=LATENCY_COPY[latency_status][1],
        model_version=prediction.model_version,
        preprocessing_version=prediction.preprocessing_version
    )


def to_user_facing_error(error: Exception, request_id: str) -> UserFacingError:
    """asigna código estable, mensaje accionable y recuperación."""

    if type(error) == InputContractError:
        return UserFacingError(code="invalid_input", title="Contrato de entrada inválido", message="La petición no cumple el contrato de entrada", recovery="Introduzca datos válidos", request_id=request_id)
    elif type(error) == ArtifactUnavailableError:
        return UserFacingError(code="artifact_unavailable", title="Modelo no disponible", message="El bundle o backend no está disponible", recovery="Vuelva a intentarlo más tarde", request_id=request_id)
    elif type(error) == InferenceTimeoutError:
        return UserFacingError(code="timeout", title="Tiempo de espera agotado", message="La inferencia tardó más de lo permitido", recovery="Vuelva a intentarlo más tarde", request_id=request_id)
    elif type(error) == BackendInferenceError:
        return UserFacingError(code="prediction_error", title="Error interno del servidor", message="El backend no produjo una salida compatible", recovery="Vuelva a intentarlo más tarde", request_id=request_id)




