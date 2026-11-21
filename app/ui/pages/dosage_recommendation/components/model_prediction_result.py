from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class ModelPredictionResult(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PredictionMonolithCard")
        self.setFixedWidth(265)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        tag = QLabel("PREDICTED DOSAGE")
        tag.setObjectName("PredictionTag")

        chemical_lbl = QLabel("Alum")
        chemical_lbl.setObjectName("ChemicalTitle")

        # Main Dosage Number + Unit inline
        dosage_row = QHBoxLayout()
        dosage_row.setContentsMargins(0, 4, 0, 2)
        dosage_row.setSpacing(6)

        self.dosage_val_lbl = QLabel("——")
        self.dosage_val_lbl.setObjectName("DosageMainValueEmpty")

        self.dosage_unit_lbl = QLabel("mg/L")
        self.dosage_unit_lbl.setObjectName("DosageMainUnit")
        self.dosage_unit_lbl.setAlignment(Qt.AlignmentFlag.AlignBottom)

        dosage_row.addWidget(self.dosage_val_lbl)
        dosage_row.addWidget(self.dosage_unit_lbl)
        dosage_row.addStretch()

        model_caption = QLabel("Predicted by ML Model")
        model_caption.setObjectName("PredictionSubtext")

        # Hairline Divider
        divider = QFrame()
        divider.setObjectName("PredictionDivider")
        divider.setFixedHeight(1)

        # Stock Solution Dispense Section
        dispense_caption = QLabel("Stock solution to dispense")
        dispense_caption.setObjectName("PredictionSubtext")

        self.volume_val_lbl = QLabel("—— mL")
        self.volume_val_lbl.setObjectName("DispenseVolumeEmpty")

        self.sample_vol_caption = QLabel("For 1 L of raw water")
        self.sample_vol_caption.setObjectName("PredictionSubtext")

        layout.addWidget(tag)
        layout.addWidget(chemical_lbl)
        layout.addLayout(dosage_row)
        layout.addWidget(model_caption)
        layout.addSpacing(10)
        layout.addWidget(divider)
        layout.addSpacing(10)
        layout.addWidget(dispense_caption)
        layout.addWidget(self.volume_val_lbl)
        layout.addWidget(self.sample_vol_caption)
        layout.addStretch()

    def set_prediction(self, data: dict | None) -> None:
        if not data or "recommendation" not in data:
            self.dosage_val_lbl.setText("——")
            self.dosage_val_lbl.setObjectName("DosageMainValueEmpty")
            self.volume_val_lbl.setText("—— mL")
            self.volume_val_lbl.setObjectName("DispenseVolumeEmpty")
            self.sample_vol_caption.setText("For 1 L of raw water")
        else:
            rec = data["recommendation"]
            dosage = float(rec["predicted_dosage"])
            volume = float(rec["volume_to_dispense"])

            self.dosage_val_lbl.setText(f"{dosage:.2f}")
            self.dosage_val_lbl.setObjectName("DosageMainValue")
            self.volume_val_lbl.setText(f"{volume:.2f} mL")
            self.volume_val_lbl.setObjectName("DispenseVolumeValue")

        for widget in (self.dosage_val_lbl, self.volume_val_lbl):
            widget.style().unpolish(widget)
            widget.style().polish(widget)