"""Políticas explícitas que el alumnado puede reutilizar en la UI."""

from dataclasses import dataclass

from model_ui.contracts import ConfidenceLevel, LatencyStatus


@dataclass(frozen=True)
class ConfidencePolicy:
    """Umbrales de comunicación, no de aprobación del modelo."""

    low_below: float = 0.60
    high_from: float = 0.85


@dataclass(frozen=True)
class LatencyPolicy:
    """Objetivo técnico de la demo."""

    target_ms: float = 300.0


DEFAULT_CONFIDENCE_POLICY = ConfidencePolicy()
DEFAULT_LATENCY_POLICY = LatencyPolicy()


def classify_confidence(
    confidence: float, policy: ConfidencePolicy = DEFAULT_CONFIDENCE_POLICY
) -> ConfidenceLevel:
    """valida [0, 1] y devuelve low/medium/high según policy."""

    if confidence < 0 or confidence > 1:
        raise ValueError("ERROR: Invalid confidence. Debe estar entre 0 y 1")
    
    if confidence < ConfidencePolicy.low_below:
        return "low"
    elif confidence >= ConfidencePolicy.high_from:
        return "high"
    else:
        return "medium"



def classify_latency(
    latency_ms: float, policy: LatencyPolicy = DEFAULT_LATENCY_POLICY
) -> LatencyStatus:
    """devuelve within_target o above_target para una latencia válida."""

    if latency_ms > LatencyPolicy.target_ms:
        return "above_target"
    else:
        return "within_target"
