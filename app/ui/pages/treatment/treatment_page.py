from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import QLabel

from pathlib import Path


class TreatmentPage(QFrame):
    def __init__(self):
        super().__init__()
        # setup the parent container style
        self.setObjectName('TreatmentAssessmentFrame')

        main_container = QVBoxLayout(self)

        self.sample_label = QLabel('Treatment Assessment Page')

        main_container.addWidget(self.sample_label)

        # load the qss
        self._load_style()

    def _load_style(self) -> None:
            qss_path = Path(__file__).parent / "styles" / "treatment_page_style.qss"
            if qss_path.exists():
                self.setStyleSheet(qss_path.read_text(encoding="utf-8"))
