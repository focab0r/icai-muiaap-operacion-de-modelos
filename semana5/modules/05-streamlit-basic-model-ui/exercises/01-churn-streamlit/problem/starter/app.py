"""Starter: conecta una función de inferencia pura con Streamlit."""

from collections.abc import Callable
from typing import Any

from src.churn_demo.model import ChurnPrediction, predict

Predictor = Callable[..., ChurnPrediction]


def collect_profile(st: Any) -> tuple[bool, dict[str, object]]:
    """Renderiza cuatro widgets dentro de un único formulario."""
    #  (alumno): usa st.form("churn_form"), los cuatro widgets con las
    # claves indicadas en el README y st.form_submit_button. El formulario evita
    # inferencias durante cada edición. Compruébalo con el primer test de app.
    
    with st.form("churn_form"):
        tenure_months = st.slider("tenure_months", key="tenure_months", min_value=0, max_value=120, value=12)
        monthly_spend_eur = st.number_input("monthly_spend_eur", key="monthly_spend_eur", min_value=0, max_value=300, value=60)
        support_calls = st.slider("support_calls", key="support_calls", min_value=0, max_value=20, value=1)
        has_annual_contract = st.checkbox("has_annual_contract", key="has_annual_contract", value=False)
        
        submit_form = st.form_submit_button(label="Calcular riesgo")

        if submit_form:
            if tenure_months and monthly_spend_eur and support_calls:
                st.write("Sucess")
                return (True, {"tenure_months": int(tenure_months),
                    "monthly_spend_eur": int(monthly_spend_eur),
                    "support_calls": int(support_calls),
                    "has_annual_contract": has_annual_contract})
            else:
                st.warning("Please fill all the fields")

    return (False, {"tenure_months": 0,
        "monthly_spend_eur": 0,
        "support_calls": 0,
        "has_annual_contract": 0})


def render_prediction(st: Any, result: ChurnPrediction) -> None:
    """Muestra etiqueta, score orientativo y explicación."""
    # 3 (alumno): presenta label, risk_score y explanation con componentes
    # Streamlit. No recalcules el score. Compruébalo con el test de presentación.
    if result["label"] == "Baja probable":
        st.warning(result["label"])
    elif result["label"] == "Permanencia probable":
        st.success(result["label"])

    st.metric("Risk Score", result["risk_score"])

    st.write(result["explanation"])





def run_app(st: Any, predictor: Predictor) -> None:
    """Conecta submit, llamada al predictor y actualización visible."""
    # 2 (alumno): llama a collect_profile, ejecuta predictor(**values) solo
    # tras el submit y una única vez; convierte ValueError en un mensaje seguro.
    # Los tests de 0/1 llamadas y de error verifican este contrato.
    submitted, values = collect_profile(st)
    if submitted:
        try:
            churn = predictor(**values)
            render_prediction(st, churn)
        except Exception as e:
            st.error("[X] ERROR: No se pudo calcular")



def main() -> None:
    """Configura la página real y delega el flujo comprobable en run_app."""
    import streamlit as st

    st.set_page_config(page_title="Churn sintético · S5", page_icon="📉")
    st.title("¿Qué cliente podría darse de baja?")
    st.caption("Caso docente sintético; el score no es una probabilidad calibrada.")
    run_app(st, predict)


if __name__ == "__main__":
    main()
