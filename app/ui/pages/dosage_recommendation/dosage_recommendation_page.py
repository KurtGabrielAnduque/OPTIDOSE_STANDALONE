from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QLabel

from pathlib import Path


class DosageRecommendationPage(QFrame):
    def __init__(self):
        super().__init__()
        # setup the container
        self.setObjectName('DosageRecomendationFrame')

        main_container = QVBoxLayout(self)

        self.sample_label = QLabel('Dosage Prediction Page')

        main_container.addWidget(self.sample_label)

        self._load_style()

    def _load_style(self) -> None:
            qss_path = Path(__file__).parent / "styles" / "dosage_recommendation_style.qss"
            if qss_path.exists():
                self.setStyleSheet(qss_path.read_text(encoding="utf-8"))
