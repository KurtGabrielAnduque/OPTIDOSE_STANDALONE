from pathlib import Path
from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy

from app.mock_data.dosage_data import dosage_recommendation_payload
from app.ui.pages.dosage_recommendation.components.bottom_action_bar import BottomActionBar
from app.ui.pages.dosage_recommendation.components.model_prediction_result import (
    ModelPredictionResult,
)
from app.ui.pages.dosage_recommendation.components.parameter_table import ParameterTable



class DosageRecommendationPage(QFrame):
    validate_dosage_requested = Signal(dict)

    def __init__(self):
        super().__init__()
        self.setObjectName("DosagePageFrame")
        self._current_data: dict | None = None
        self._analysis_timer = QTimer(self)
        self._analysis_timer.setSingleShot(True)
        self._analysis_timer.timeout.connect(
            self._on_analysis_complete
        )

        self._load_style()
        self._setup_ui()

    def _load_style(self) -> None:
        qss_path = Path(__file__).parent / "styles" / "dosage_recommendation_style.qss"
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        # 1. Top Header
        root.addLayout(self._build_header())

        top_divider = QFrame()
        top_divider.setObjectName("HairlineDivider")
        top_divider.setFixedHeight(1)
        root.addWidget(top_divider)

        # 2. Main Split Body (Left Telemetry Grid + Right Black Dosage Monolith)
        body_row = QHBoxLayout()
        body_row.setSpacing(14)

        self.parameter_table = ParameterTable()
        self.prediction_panel = ModelPredictionResult()

        # Allow the components to expand vertically
        self.parameter_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.prediction_panel.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding
        )


        body_row.addWidget(self.parameter_table, stretch=1)
        body_row.addWidget(self.prediction_panel, stretch=0)
        # Give the body all remaining vertical space
        root.addLayout(body_row, stretch=1)


        # 3. Bottom Divider + Action Bar
        bottom_divider = QFrame()
        bottom_divider.setObjectName("HairlineDivider")
        bottom_divider.setFixedHeight(1)
        root.addWidget(bottom_divider)

        self.action_bar = BottomActionBar()
        root.addWidget(self.action_bar)

        # Connect Signals
        self.action_bar.start_clicked.connect(self._handle_start_analysis)
        self.action_bar.reset_clicked.connect(self._reset)
        self.action_bar.validate_clicked.connect(self._handle_validate)

    def _build_header(self) -> QVBoxLayout:
        header = QVBoxLayout()
        header.setSpacing(2)

        eyebrow = QLabel("WATER ANALYSIS")
        eyebrow.setObjectName("HeaderEyebrow")

        title = QLabel("Water Analysis & Dosage Prediction")
        title.setObjectName("HeaderTitle")

        subtitle = QLabel(
            "Analyze raw water quality and review the predicted dosage by the machine learning model"
        )
        subtitle.setObjectName("HeaderSubtitle")

        note = QLabel("Note: Please ensure a 1L raw-water sample is placed in the chamber before analysis")
        note.setObjectName("HeaderNote")

        header.addWidget(eyebrow)
        header.addWidget(title)
        header.addSpacing(2)
        header.addWidget(subtitle)
        header.addWidget(note)
        return header

    def _handle_start_analysis(self) -> None:
        if not self.action_bar.is_sample_secured():
            self.action_bar.show_sample_warning()
            return

        self._current_data = None
        self.parameter_table.set_state("analyzing")
        self.prediction_panel.set_prediction(None)
        self.action_bar.set_state("analyzing")

        # Simulated 1.5s sensor & ML inference delay
        self._analysis_timer.start(2000)

    def _on_analysis_complete(self) -> None:
        self.show_prediction(dosage_recommendation_payload)

    def show_prediction(self, data: dict) -> None:
        self._current_data = data
        self.parameter_table.set_state("complete", self._current_data)
        self.prediction_panel.set_prediction(self._current_data)
        self.action_bar.set_state("complete")

    def _handle_validate(self) -> None:
        if self._current_data:
            self.validate_dosage_requested.emit(self._current_data)

    def _reset(self) -> None:
        self._analysis_timer.stop()
        self._current_data = None
        self.parameter_table.set_state("idle")
        self.prediction_panel.set_prediction(None)
        self.action_bar.set_state("idle")