"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
import joblib
import json
import os

from pydantic import BaseModel, ConfigDict, Field, field_validator
from model_packaging.preprocess import preprocess_wine_request, PREPROCESSING_VERSION, FEATURE_NAMES

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1"
DEFAULT_BUNDLE_PATH = Path("models/wine_quality_bundle")
MANIFEST_FILENAME = "manifest.json"
MODEL_FILENAME = "model.joblib"
OUTPUT_LABELS: tuple[QualityBand, ...] = (
    "needs_review",
    "acceptable",
    "excellent",
)


class WineQualityEstimator(Protocol):
    """Interfaz mínima que debe cumplir el estimador cargado."""

    def predict(self, features: list[list[float]]) -> Sequence[str]:
        """Devuelve una etiqueta por fila."""

    def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
        """Devuelve probabilidades por fila."""



class ArtifactManifest(BaseModel):

    model_config = ConfigDict(extra="forbid")

    schema_version: str
    model_version: str = Field(min_length=1)
    preprocessing_version: str
    feature_names: tuple[str, ...]
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)

    @field_validator('feature_names', mode="before")
    def check_feature_names(cls, feature_names):
        if feature_names != FEATURE_NAMES:
            raise ValueError("Invalid features")
        return feature_names

    def to_dict(self):

        feature_names_list = []
        for elem in self.feature_names:
            feature_names_list.append(elem)
        output_labels_list = []
        for elem in self.output_labels:
            output_labels_list.append(elem)    
        return {
            "schema_version": self.schema_version,
            "model_version": self.model_version,
            "preprocessing_version": self.preprocessing_version,
            "feature_names": feature_names_list,
            "output_labels": output_labels_list,
            "estimator_type": self.estimator_type
        }

@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest




def create_manifest(estimator: WineQualityEstimator, model_version: str) -> ArtifactManifest:
    """Devuelve un manifiesto compatible con el contrato."""

    return ArtifactManifest(
        schema_version = ARTIFACT_SCHEMA_VERSION,
        model_version = model_version,
        preprocessing_version = PREPROCESSING_VERSION,
        feature_names = FEATURE_NAMES,
        output_labels = OUTPUT_LABELS,
        estimator_type = type(estimator).__name__
    )

    raise NotImplementedError("Implementa create_manifest().")

def _load_model(path_to_model: Path):
    diccionario = {"estimator": estimator, model_version: ""}
    model = joblib.dump()
    return 

def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,
    manifest: ArtifactManifest | None = None,
) -> ArtifactManifest:

    if manifest is not None:

        manifest_json = manifest.to_dict()

        bundle_path.mkdir(exist_ok=True)                                       # Create folder if it doesnt exists
        with open(bundle_path / "manifest.json", "w+") as m:
            #json.dump(manifest_json, m, indent=4, ensure_ascii=False)
            json.dump(manifest_json, m)
    else:
        Exception("[X] ERROR: Unable to save manifest. Invalid manifest")

    if estimator is not None:
        joblib.dump(estimator, bundle_path / "model.joblib")
    else:
        Exception("[X] ERROR: Unable to save estimator. Invalid estimator")

    return manifest




def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """TODO: valida el manifiesto antes de cargar el estimador."""

    with open(bundle_path / "manifest.json", "r") as m:
        manifest_str = m.read()

    manifest_json = json.loads(manifest_str)
    manifest = ArtifactManifest(
        schema_version=manifest_json['schema_version'],
        model_version=manifest_json['model_version'],
        preprocessing_version=manifest_json['preprocessing_version'],
        feature_names=tuple(manifest_json['feature_names']),
        output_labels=tuple(manifest_json['output_labels']),
        estimator_type=manifest_json['estimator_type'])
    
    estimator = joblib.load(bundle_path / "model.joblib")
    l = LoadedModelBundle(estimator=estimator, manifest=manifest)
    return l


def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """TODO: preprocesa, invoca el estimador y valida la respuesta."""

    w = preprocess_wine_request(request)

    manifest = bundle.manifest
    estimator = bundle.estimator

    quality_band = estimator.predict(w.as_vector())
    confidence = estimator.predict_proba(w.as_vector())
    w = WineQualityPrediction(
        quality_band=quality_band[0],
        confidence=confidence[0][0],
        model_version=manifest.model_version,
        preprocessing_version=manifest.preprocessing_version
    )

    return w
