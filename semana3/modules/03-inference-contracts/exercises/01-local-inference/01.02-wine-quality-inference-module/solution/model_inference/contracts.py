"""TODO: contratos de entrada y salida de la inferencia."""

# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.


from pydantic import BaseModel, Field, field_validator, ConfigDict



class WineQualityRequest(BaseModel):

	model_config = ConfigDict(extra="forbid")

	sample_id: 				str = Field(min_length=1)
	fixed_acidity:			float = Field(gt=0, le=20)
	volatile_acidity:		float = Field(ge=0, le=1)
	citric_acid:			float = Field(ge=0, le=1)
	residual_sugar:			float = Field(gt=0, le=100)
	chlorides:				float = Field(ge=0, le=1)
	free_sulfur_dioxide:	float = Field(gt=0, le=100)
	total_sulfur_dioxide:	float = Field(gt=0, le=100)
	density:				float = Field(ge=0, le=1)
	ph:						float = Field(gt=0, le=100)
	sulphates:				float = Field(ge=0, le=1)
	alcohol:				float = Field(gt=0, le=100)

	