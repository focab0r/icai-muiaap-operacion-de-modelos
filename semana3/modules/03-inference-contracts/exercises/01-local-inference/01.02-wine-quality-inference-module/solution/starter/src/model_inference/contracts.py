"""TODO: contratos de entrada y salida de la inferencia."""

# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.


from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

import pandas as pd


class WineQualityRequest(BaseModel):

	model_config = ConfigDict(extra="forbid")

	sample_id: 				Optional[str] = None
	fixed_acidity:			float = Field(gt=0, le=20)
	volatile_acidity:		float = Field(ge=0, le=2)
	citric_acid:			float = Field(ge=0, le=2)
	residual_sugar:			float = Field(gt=0, le=20)
	chlorides:				float = Field(ge=0, le=1)
	free_sulfur_dioxide:	float = Field(gt=0, le=100)
	total_sulfur_dioxide:	float = Field(gt=0, le=300)
	density:				float = Field(ge=0.98, le=1.01)
	ph:						float = Field(gt=2.5, le=4.5)
	sulphates:				float = Field(ge=0, le=3)
	alcohol:				float = Field(gt=5, le=20)

	# @field_validator("sample_id", mode="before")
	# @classmethod
	# def empty_is_none(cls, value):
	# 	if value == pd.isna(value):
	# 		return None
	# 	return value