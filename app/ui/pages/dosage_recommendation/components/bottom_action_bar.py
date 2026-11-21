from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QPushButton


class SampleChamberSwitch(QCheckBox):
    """High-contrast monochrome toggle switch for chamber sample confirmation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track = QColor("#09090B") if self.isChecked() else QColor("#D4D4D8")
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(track)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 11, 11)

        knob_x = self.width() - 19 if self.isChecked() else 3
        painter.setBrush(QColor("#FFFFFF"))
        painter.drawEllipse(knob_x, 3, 16, 16)
        painter.end()


class BottomActionBar(QFrame):
    start_clicked = Signal()
    reset_clicked = Signal()
    validate_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("BottomActionBar")
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(12)

        # --- IDLE WIDGETS ---
        self.chamber_box = QFrame()
        self.chamber_box.setObjectName("ChamberConfirmBox")
        self.chamber_box.setFixedHeight(42)
        self.chamber_box.setCursor(Qt.CursorShape.PointingHandCursor)
        self.chamber_box.mousePressEvent = lambda _event: self.chamber_switch.toggle()
        chamber_layout = QHBoxLayout(self.chamber_box)
        chamber_layout.setContentsMargins(12, 0, 12, 0)
        chamber_layout.setSpacing(10)

        self.chamber_switch = SampleChamberSwitch()
        self.chamber_switch.toggled.connect(self._on_toggled)

        self.chamber_lbl = QLabel("Check only if 1L raw-water sample is secured in chamber")
        self.chamber_lbl.setObjectName("ChamberLabelNormal")

        chamber_layout.addWidget(self.chamber_switch)
        chamber_layout.addWidget(self.chamber_lbl)
        chamber_layout.addStretch()

        self.start_btn = QPushButton("Start Water Analysis")
        self.start_btn.setObjectName("PrimaryBlackBtn")
        self.start_btn.setFixedHeight(42)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.clicked.connect(self.start_clicked.emit)

        # --- ANALYZING WIDGET ---
        self.analyzing_btn = QPushButton("Analyzing Water Sample & Running ML Model...")
        self.analyzing_btn.setObjectName("AnalyzingDisabledBtn")
        self.analyzing_btn.setFixedHeight(42)
        self.analyzing_btn.setEnabled(False)

        # --- COMPLETE WIDGETS (Matches Figma Screenshot) ---
        self.reset_btn = QPushButton("Perform New Analysis")
        self.reset_btn.setObjectName("SecondaryOutlineBtn")
        self.reset_btn.setFixedHeight(42)
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.reset_clicked.emit)

        self.validate_btn = QPushButton("Validate Predicted Dosage")
        self.validate_btn.setObjectName("PrimaryBlackBtn")
        self.validate_btn.setFixedHeight(42)
        self.validate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.validate_btn.clicked.connect(self.validate_clicked.emit)

        # Add all to horizontal bar (equal 50/50 stretch)
        layout.addWidget(self.chamber_box, stretch=1)
        layout.addWidget(self.start_btn, stretch=1)
        layout.addWidget(self.analyzing_btn, stretch=1)
        layout.addWidget(self.reset_btn, stretch=1)
        layout.addWidget(self.validate_btn, stretch=1)

        self.set_state("idle")

    def _on_toggled(self, checked: bool) -> None:
        self.chamber_box.setObjectName("ChamberConfirmBoxChecked" if checked else "ChamberConfirmBox")
        self.chamber_lbl.setObjectName("ChamberLabelChecked" if checked else "ChamberLabelNormal")
        self.chamber_lbl.setText(
            "1L raw-water sample secured in chamber"
            if checked
            else "Check only if 1L raw-water sample is secured in chamber"
        )
        for w in (self.chamber_box, self.chamber_lbl):
            w.style().unpolish(w)
            w.style().polish(w)

    def show_sample_warning(self) -> None:
        self.chamber_box.setObjectName("ChamberConfirmBoxWarning")
        self.chamber_lbl.setObjectName("ChamberLabelWarning")
        self.chamber_lbl.setText("⚠ Please confirm 1L sample is secured in chamber first")
        for w in (self.chamber_box, self.chamber_lbl):
            w.style().unpolish(w)
            w.style().polish(w)

    def is_sample_secured(self) -> bool:
        return self.chamber_switch.isChecked()

    def set_state(self, state: str) -> None:
        is_idle = state == "idle"
        is_analyzing = state == "analyzing"
        is_complete = state == "complete"

        if is_idle:
            self.chamber_switch.setChecked(False)
            self._on_toggled(False)

        self.chamber_box.setVisible(is_idle)
        self.start_btn.setVisible(is_idle)
        self.analyzing_btn.setVisible(is_analyzing)
        self.reset_btn.setVisible(is_complete)
        self.validate_btn.setVisible(is_complete)