from pydantic import BaseModel, Field, field_validator


class WineInputSchema(BaseModel):
    sample_id: int  = Field(description="Unique identifier")
    fixed_acidit: float = Field(description="fixed_acidit attribute")
    volatile_acidity: float = Field(description="volatile_acidity attribute")
    citric_acid: float = Field(description="citric_acid attribute")
    residual_sugar: float = Field(description="residual_sugar attribute")
    chlorides: float = Field(description="chlorides attribute")
    free_sulfur_dioxide: float = Field(description="free_sulfur_dioxide attribute")
    total_sulfur_dioxide: float = Field(description="total_sulfur_dioxide attribute")
    density: float = Field(description="density attribute")
    ph: float = Field(description="ph attribute")
    sulphates: float = Field(description="sulphates attribute")
    alcohol: float = Field(description="alcohol attribute")


if __name__ == "__main__":
    mi_contrato = WineInputSchema(
        sample_id=1,
        fixed_acidit=2,
        volatile_acidity=3,
        citric_acid=4,
        residual_sugar=5,
        chlorides=6,
        free_sulfur_dioxide=7,
        total_sulfur_dioxide=8,
        density=9,
        ph=10,
        sulphates=11,
        alcohol=12
        )