"""Estado de sesión de Streamlit aislado para poder probarlo sin Streamlit."""

from __future__ import annotations

from collections.abc import MutableMapping

from model_ui.telemetry import Telemetry
from model_ui.contracts import UiState

LAST_STATE_KEY = "last_state"
TELEMETRY_KEY = "telemetry"
LAST_VALUES_KEY = "last_values"


def initialize_session_state(
    session_state: MutableMapping[str, object],
) -> None:
    """crea solo las entradas de sesión que todavía no existan."""
    session_state[LAST_STATE_KEY] = UiState(phase="idle")
    if TELEMETRY_KEY not in session_state.keys():
        session_state[TELEMETRY_KEY] = Telemetry()
    session_state[LAST_VALUES_KEY] = {}


def clear_last_state(session_state: MutableMapping[str, object]) -> None:
    """vuelve a idle sin perder la telemetría acumulada."""

    session_state[LAST_STATE_KEY] = UiState(phase="idle")
    session_state[LAST_VALUES_KEY] = {}
