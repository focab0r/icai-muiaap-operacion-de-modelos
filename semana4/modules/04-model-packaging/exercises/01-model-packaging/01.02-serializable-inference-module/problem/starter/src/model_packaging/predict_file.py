"""Punto de extensión del CLI de inferencia sobre un bundle."""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from model_packaging.artifact import DEFAULT_BUNDLE_PATH, load_model_bundle, infer_wine_quality
from model_packaging.contracts import WineQualityRequest


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:

    df = pd.read_csv(input_path)
    df = df.drop(columns="sample_id")
    bundle = load_model_bundle(bundle_path)
    
    df_dict = df.to_dict(orient='index')
    wine_quality_list = []
    for elem in df_dict.values():
        w = WineQualityRequest(**elem)
        wine_quality = infer_wine_quality(bundle, w)
        wine_quality_list.append(wine_quality)
    
    flag = 0
    with open(output_path, "w+") as f:
        f.write("quality_band,confidence,model_version,preprocessing_version")
        for elem in wine_quality_list:
            f.write(f'{elem.quality_band},{elem.confidence},{elem.model_version},{elem.preprocessing_version}\n')
            flag+=1
    
    return flag




def parse_args() -> argparse.Namespace:
    """Declara la interfaz del comando público."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    raise SystemExit(
        predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    )
