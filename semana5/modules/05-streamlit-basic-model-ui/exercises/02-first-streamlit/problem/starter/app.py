"""Starter de la primera interfaz Streamlit para Wine Quality."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from model_ui.contracts import PredictionPayload
from model_ui.errors import ArtifactUnavailableError, InputContractError
from model_ui.gateway import InferenceGateway, PackagedBundleGateway
from model_ui.ui_schema import FIELD_SPECS


def build_gateway() -> InferenceGateway:
    """Carga obligatoriamente el bundle de S4 configurado."""

    bundle_value = os.getenv("MODEL_UI_BUNDLE")
    if not bundle_value:
        raise ArtifactUnavailableError("MODEL_UI_BUNDLE no está configurado.")
    try:
        return PackagedBundleGateway.from_bundle_path(Path(bundle_value))
    except Exception as error:  # noqa: BLE001
        raise ArtifactUnavailableError("No se pudo cargar el bundle de S4.") from error


def render_bundle_error(st: Any) -> None:
    """Presenta una recuperación segura sin revelar detalles internos."""

    st.error("No se pudo cargar el bundle de S4.")
    st.info("Configura MODEL_UI_BUNDLE y vuelve a ejecutar la aplicación.")


def render_inference_error(st: Any) -> None:
    """Presenta un fallo de validación o inferencia sin detalles sensibles."""

    st.error("No se pudo ejecutar la inferencia.")
    st.info("Revisa los datos y la compatibilidad del bundle de S4.")


def collect_values(st: Any) -> tuple[bool, dict[str, float]]:
    """renderiza ``FIELD_SPECS`` dentro de un único ``st.form``.

    Cada ``number_input`` debe recibir label, rango, default, step y una key
    estable. Devuelve ``(submitted, values)`` sin llamar al gateway.
    """

    with st.form("wine_quality_form"):

        fixed_acidity = st.number_input(FIELD_SPECS[0].label, key="input_"+FIELD_SPECS[0].name, value=FIELD_SPECS[0].default, min_value=FIELD_SPECS[0].min_value, max_value=FIELD_SPECS[0].max_value, step=FIELD_SPECS[0].step)
        volatile_acidity = st.number_input(FIELD_SPECS[1].label, key="input_"+FIELD_SPECS[1].name, value=FIELD_SPECS[1].default, min_value=FIELD_SPECS[1].min_value, max_value=FIELD_SPECS[1].max_value, step=FIELD_SPECS[1].step)
        citric_acid = st.number_input(FIELD_SPECS[2].label, key="input_"+FIELD_SPECS[2].name, value=FIELD_SPECS[2].default, min_value=FIELD_SPECS[2].min_value, max_value=FIELD_SPECS[2].max_value, step=FIELD_SPECS[2].step)
        residual_sugar = st.number_input(FIELD_SPECS[3].label, key="input_"+FIELD_SPECS[3].name, value=FIELD_SPECS[3].default, min_value=FIELD_SPECS[3].min_value, max_value=FIELD_SPECS[3].max_value, step=FIELD_SPECS[3].step)

        chlorides = st.number_input(FIELD_SPECS[4].label, key="input_"+FIELD_SPECS[4].name, value=FIELD_SPECS[4].default, min_value=FIELD_SPECS[4].min_value, max_value=FIELD_SPECS[4].max_value, step=FIELD_SPECS[4].step)
        free_sulfur_dioxide = st.number_input(FIELD_SPECS[5].label, key="input_"+FIELD_SPECS[5].name, value=FIELD_SPECS[5].default, min_value=FIELD_SPECS[5].min_value, max_value=FIELD_SPECS[5].max_value, step=FIELD_SPECS[5].step)
        total_sulfur_dioxide = st.number_input(FIELD_SPECS[6].label, key="input_"+FIELD_SPECS[6].name, value=FIELD_SPECS[6].default, min_value=FIELD_SPECS[6].min_value, max_value=FIELD_SPECS[6].max_value, step=FIELD_SPECS[6].step)
        density = st.number_input(FIELD_SPECS[7].label, key="input_"+FIELD_SPECS[7].name, value=FIELD_SPECS[7].default, min_value=FIELD_SPECS[7].min_value, max_value=FIELD_SPECS[7].max_value, step=FIELD_SPECS[7].step)

        ph = st.number_input(FIELD_SPECS[8].label, key="input_"+FIELD_SPECS[8].name, value=FIELD_SPECS[8].default, min_value=FIELD_SPECS[8].min_value, max_value=FIELD_SPECS[8].max_value, step=FIELD_SPECS[8].step)
        sulphates = st.number_input(FIELD_SPECS[9].label, key="input_"+FIELD_SPECS[9].name, value=FIELD_SPECS[9].default, min_value=FIELD_SPECS[9].min_value, max_value=FIELD_SPECS[9].max_value, step=FIELD_SPECS[9].step)
        alcohol = st.number_input(FIELD_SPECS[10].label, key="input_"+FIELD_SPECS[10].name, value=FIELD_SPECS[10].default, min_value=FIELD_SPECS[10].min_value, max_value=FIELD_SPECS[10].max_value, step=FIELD_SPECS[10].step)
        
        submit_form = st.form_submit_button(label="Ejecutar inferencia")

        if submit_form:
            if fixed_acidity and volatile_acidity and citric_acid and residual_sugar and chlorides and free_sulfur_dioxide and total_sulfur_dioxide and density and ph and sulphates and alcohol:
                st.write("Success")
                return(True, {
                    "fixed_acidity": fixed_acidity,
                    "volatile_acidity": volatile_acidity,
                    "citric_acid": citric_acid,
                    "residual_sugar": residual_sugar,
                    "chlorides": chlorides,
                    "free_sulfur_dioxide": free_sulfur_dioxide,
                    "total_sulfur_dioxide": total_sulfur_dioxide,
                    "density": density,
                    "ph": ph,
                    "sulphates": sulphates,
                    "alcohol": alcohol
                })
            else:
                st.warning("Please fill all the fields")
        
    return(False, {
        "fixed_acidity": 0,
        "volatile_acidity": 0,
        "citric_acid": 0,
        "residual_sugar": 0,
        "chlorides": 0,
        "free_sulfur_dioxide": 0,
        "total_sulfur_dioxide": 0,
        "density": 0,
        "ph": 0,
        "sulphates": 0,
        "alcohol": 0
    })

def render_prediction(st: Any, prediction: PredictionPayload) -> None:
    """TODO: presenta los cuatro campos de ``PredictionPayload``."""

    st.write("quality_band: " + prediction.quality_band)
    st.write("confidence: " + str(prediction.confidence))
    st.write("model_version: " + prediction.model_version)
    st.write("preprocessing_version: " + prediction.preprocessing_version)


def run_app(st: Any, gateway: InferenceGateway) -> None:
    """Conecta submit, gateway y salida sin añadir estado avanzado."""

    submitted, values = collect_values(st)
    if not submitted:
        st.info("Completa el formulario y pulsa «Ejecutar inferencia».")
        return

    try:
        prediction = gateway.predict(values)
    except ArtifactUnavailableError:
        render_bundle_error(st)
        return
    except InputContractError:
        render_inference_error(st)
        return
    except ValueError:
        render_inference_error(st)
        return

    render_prediction(st, prediction)


def run_configured_app(
    st: Any,
    gateway_factory: Callable[[], InferenceGateway] = build_gateway,
) -> None:
    """Carga la configuración y contiene cualquier fallo del bundle."""

    try:
        gateway = gateway_factory()
    except ArtifactUnavailableError:
        render_bundle_error(st)
        return
    run_app(st, gateway)


def main() -> None:
    """Ejecuta la pantalla básica; S6 añadirá estado explícito."""

    try:
        import streamlit as st
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Instala Streamlit con `uv run --with streamlit streamlit run app.py`."
        ) from error

    st.set_page_config(page_title="Wine Quality · S5", page_icon="🍷")
    st.title("Primera interfaz de inferencia")
    st.caption("S5: formulario, gateway y resultado; el estado avanzado llega en S6.")

    run_configured_app(st)


if __name__ == "__main__":
    main()
