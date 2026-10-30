from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator, ValidationError


# clase PrestamoEntrada (BaseModel) con las 6 variables del modelo, con sus rangos (ver enunciado).
#       Debe rechazar campos que no existan.
# field_validator (con classmethod) para antiguedad_laboral_anios: no puede ser incoherente con la edad.
# clase PrediccionSalida con probabilidad_impago (entre 0 y 1) y decision (aprobar, revisar o rechazar).


class PrestamoEntrada(BaseModel):
    
    model_config = ConfigDict(extra="forbid")

    edad:                       int = Field(ge=18, le=75)
    ingresos_mensuales:         float = Field(gt=0)
    importe_prestamo:           float = Field(gt=0)
    plazo_meses:                int = Field(ge=6, le=84)
    antiguedad_laboral_anios:   int = Field(ge=0, le=50)
    impagos_previos:            int = Field(ge=0, le=20)

    @model_validator(mode="after")
    def set_antiguedad_laboral_anios(self):
        if self.edad - 16 < self.antiguedad_laboral_anios:
            raise ValueError("[X] ERROR: Invalid antiguedad_laboral")
        return self

    def to_vector(self):
        return [[
            self.edad,
            self.ingresos_mensuales,
            self.importe_prestamo,
            self.plazo_meses,
            self.antiguedad_laboral_anios,
            self.impagos_previos
        ]]

class PrediccionSalida(BaseModel):

    model_config = ConfigDict(extra="forbid")

    probabilidad_impago:    float = Field(ge=0, le=1)
    decision:               Literal["aprobar", "rechazar", "revisar"]

    def as_dict(self):
        return {
            "probabilidad_impago": self.probabilidad_impago,
            "decision": self.decision
        }