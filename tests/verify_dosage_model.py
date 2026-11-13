
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from app.ml_models.custom_estimators import ResidualEnhancedEnsemble


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    ROOT_DIR / "app" / "ml_models" /
    "dosage_models" / "best_design_portable.pkl"
)

SCALER_PATH = (
    ROOT_DIR / "app" / "ml_models" /
    "dosage_models" / "optidose_scaler_portable.pkl"
)





# --------------------------------------------------
# 3. Expected model features
# --------------------------------------------------

MODEL_FEATURES = [
    "Conductivity (uS/cm)",
    "pH Raw",
    "Temperature (C) Raw",
    "Raw Turbidity"
]


# --------------------------------------------------
# 4. Verify model files
# --------------------------------------------------

print("\n===================================")
print("OPTIDOSE MODEL COMPATIBILITY TEST")
print("===================================")

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found: {MODEL_PATH}"
    )

if not SCALER_PATH.exists():
    raise FileNotFoundError(
        f"Scaler not found: {SCALER_PATH}"
    )

print("[OK] Model file found")
print("[OK] Scaler file found")


# --------------------------------------------------
# 5. Load model and scaler
# --------------------------------------------------

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

print("[OK] ML model loaded")
print("[OK] Scaler loaded")

print("Model class:", type(model))
print("Scaler class:", type(scaler))


# --------------------------------------------------
# 6. Test prediction
# --------------------------------------------------

# Example readings from a previous OptiDose
# sensor measurement. Use the same values when
# testing in both Conda environments.

test_data = pd.DataFrame(
    [{
        "Conductivity (uS/cm)": 37.08,
        "pH Raw": 7.72,
        "Temperature (C) Raw": 22.19,
        "Raw Turbidity": 498.65
    }],
    columns=MODEL_FEATURES
)

print("\nInput data:")
print(test_data)

scaled_data = scaler.transform(test_data)

prediction = model.predict(scaled_data)

if not np.all(np.isfinite(prediction)):
    raise ValueError("Model returned invalid prediction.")

raw_prediction = float(prediction[0])
final_dose = max(0.0, raw_prediction)

print("\n===================================")
print("PREDICTION TEST RESULTS")
print("===================================")

print(f"Raw prediction: {raw_prediction:.6f} mg/L")
print(f"Final dosage:   {final_dose:.6f} mg/L")

print("\n[ SUCCESS ]")
print("Model loading and prediction completed.")
print("Model module:", type(model).__module__)