"""TODOs del controlador de estados independiente de Streamlit."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from os import error
from time import perf_counter
from uuid import uuid4

from model_ui import gateway
from model_ui import telemetry
from model_ui.contracts import UiState
from model_ui.gateway import InferenceGateway
from model_ui.presentation import build_prediction_view, to_user_facing_error
from model_ui.telemetry import Telemetry

StateEmitter = Callable[[UiState], None]
Clock = Callable[[], float]
RequestIdFactory = Callable[[], str]


class PredictionController:
    """Orquesta loading, gateway, errores y telemetría."""

    def __init__(
        self,
        gateway: InferenceGateway,
        *,
        telemetry: Telemetry | None = None,
        clock: Clock = perf_counter,
        request_id_factory: RequestIdFactory | None = None,
    ) -> None:
        self.gateway = gateway
        self.telemetry = telemetry or Telemetry()
        self._clock = clock
        self._request_id_factory = request_id_factory or (lambda: uuid4().hex[:10])

    def submit(
        self,
        values: Mapping[str, object],
        *,
        emit: StateEmitter | None = None,
    ) -> UiState:
        """emite loading, mide, valida la salida y devuelve success/error."""

        emit(UiState(phase="loading", request_id=self._request_id_factory()))
        time1 = self._clock()
        time2 = self._clock()
        latency_ms = round((time2-time1)*1000, 0)
        try:
            pred = self.gateway.predict(values=values)
            view = build_prediction_view(pred, latency_ms)
            self.telemetry.record_success(
                latency_ms=view.latency_ms,
                model_version=view.model_version,
                preprocessing_version=view.preprocessing_version
                )
            emit(UiState(phase="success", request_id=self._request_id_factory(), view=view))
            return UiState(phase="success", request_id=self._request_id_factory(), view=view)
        except Exception as e:
            error = to_user_facing_error(e, self._request_id_factory())
            self.telemetry.record_error(
                code=error.code,
                latency_ms=latency_ms
            )
            emit(UiState(phase="error", request_id=self._request_id_factory(), error=error))
            return UiState(phase="error", request_id=self._request_id_factory(), error=error)