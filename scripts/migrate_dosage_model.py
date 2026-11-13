
import sys
from pathlib import Path

import joblib

from app.ml_models.custom_estimators import ResidualEnhancedEnsemble


ROOT_DIR = Path(__file__).resolve().parents[1]

MODEL_DIR = ROOT_DIR / "app" / "ml_models" / "dosage_models"

ORIGINAL_MODEL = MODEL_DIR / "best_design.pkl"
ORIGINAL_SCALER = MODEL_DIR / "optidose_scaler.pkl"

NEW_MODEL = MODEL_DIR / "best_design_portable.pkl"
NEW_SCALER = MODEL_DIR / "optidose_scaler_portable.pkl"


def main():
    # Register the class for loading the legacy artifact.
    sys.modules["__main__"].ResidualEnhancedEnsemble = (
        ResidualEnhancedEnsemble
    )

    # Verify source files.
    for path in [ORIGINAL_MODEL, ORIGINAL_SCALER]:
        if not path.is_file():
            raise FileNotFoundError(path)

    # Never overwrite an existing migrated artifact.
    for path in [NEW_MODEL, NEW_SCALER]:
        if path.exists():
            raise FileExistsError(
                f"Output already exists: {path}"
            )

    print("Loading original model...")
    model = joblib.load(ORIGINAL_MODEL)

    print("Loading original scaler...")
    scaler = joblib.load(ORIGINAL_SCALER)

    # Verify the custom class has a permanent module path.
    print("Model class:", type(model))
    print("Model module:", type(model).__module__)

    if type(model).__module__ != (
        "app.ml_models.custom_estimators"
    ):
        raise RuntimeError(
            "Unexpected model class module."
        )

    # Save new artifacts without modifying originals.
    joblib.dump(model, NEW_MODEL)
    joblib.dump(scaler, NEW_SCALER)

    print("\nMigration completed.")
    print("New model:", NEW_MODEL)
    print("New scaler:", NEW_SCALER)


if __name__ == "__main__":
    main()
