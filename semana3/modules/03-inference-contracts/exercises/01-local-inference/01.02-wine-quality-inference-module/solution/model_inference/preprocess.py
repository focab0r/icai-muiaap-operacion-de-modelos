"""TODO: transformación de una muestra validada en el vector del modelo."""

from model_inference.contracts import WineQualityRequest

PREPROCESSING_VERSION = 1.0

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
FEATURE_NAMES = (
	"fixed_acidity",
	"volatile_acidity",
	"citric_acid",
	"residual_sugar",
	"chlorides",
	"free_sulfur_dioxide",
	"total_sulfur_dioxide",
	"density",
	"ph",
	"sulphates",
	"alcohol",
)

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.

def preprocess_wine_request(r: WineQualityRequest):

	l = [r.fixed_acidity, r.volatile_acidity, r.citric_acid, r.residual_sugar, r.chlorides, r.free_sulfur_dioxide, r.total_sulfur_dioxide, r.density, r.ph, r.sulphates, r.alcohol]
	return l

