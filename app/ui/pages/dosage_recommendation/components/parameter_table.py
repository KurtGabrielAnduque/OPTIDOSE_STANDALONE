from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy

TOP_ROW_PARAMS = [
    ("Turbidity", "turbidity", "NTU"),
    ("pH", "ph", "—"),
    ("Conductivity", "conductivity", "µS/cm"),
]

BOTTOM_ROW_PARAMS = [
    ("Temperature", "temperature", "°C"),
    ("Alkalinity", "alkalinity", "mg/L"),
]


class TelemetryCard(QFrame):
    """Individual bordered parameter box matching the Figma telemetry cards."""

    def __init__(self, label: str, unit: str, parent=None):
        super().__init__(parent)
        self.setObjectName("TelemetryCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)

        self.name_lbl = QLabel(label)
        self.name_lbl.setObjectName("TelemetryLabel")

        self.value_lbl = QLabel("--")
        self.value_lbl.setObjectName("TelemetryValueEmpty")

        self.unit_lbl = QLabel(unit)
        self.unit_lbl.setObjectName("TelemetryUnit")

        layout.addWidget(self.name_lbl)
        layout.addWidget(self.value_lbl)
        layout.addWidget(self.unit_lbl)

    def set_value(self, value: float | int | None) -> None:
        if value is None:
            self.value_lbl.setText("--")
            self.value_lbl.setObjectName("TelemetryValueEmpty")
        else:
            formatted = f"{value:.2f}" if isinstance(value, (float, int)) else str(value)
            self.value_lbl.setText(formatted)
            self.value_lbl.setObjectName("TelemetryValue")

        self.value_lbl.style().unpolish(self.value_lbl)
        self.value_lbl.style().polish(self.value_lbl)


class ParameterTable(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LeftTelemetryColumn")
        self._cards: dict[str, TelemetryCard] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        # TAKEOVER THE REMAINING SPACE
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(10)

        # 1. Top Black Sample ID & Status Bar
        status_bar = QFrame()
        status_bar.setObjectName("SampleStatusBar")
        status_bar.setFixedHeight(44)
        bar_layout = QHBoxLayout(status_bar)
        bar_layout.setContentsMargins(14, 0, 14, 0)
        bar_layout.setSpacing(6)

        id_prefix = QLabel("Sample ID:")
        id_prefix.setObjectName("SampleIdPrefix")

        self.sample_id_lbl = QLabel("Waiting for analysis")
        self.sample_id_lbl.setObjectName("SampleIdText")

        self.status_lbl = QLabel("Status: Ready")
        self.status_lbl.setObjectName("SampleStatusText")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        bar_layout.addWidget(id_prefix)
        bar_layout.addWidget(self.sample_id_lbl)
        bar_layout.addStretch()
        bar_layout.addWidget(self.status_lbl)
        root.addWidget(status_bar)

        # 2. Row 1: 3 Cards (Turbidity, pH, Conductivity)
        row1 = QHBoxLayout()
        row1.setSpacing(10)
        for label, key, unit in TOP_ROW_PARAMS:
            card = TelemetryCard(label, unit)
            card.setSizePolicy( QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self._cards[key] = card
            row1.addWidget(card, stretch=1)

        root.addLayout(row1, stretch=1)

        # 3. Row 2: 2 Cards (Temperature, Alkalinity)
        row2 = QHBoxLayout()
        row2.setSpacing(10)
        for label, key, unit in BOTTOM_ROW_PARAMS:
            card = TelemetryCard(label, unit)
            card.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
            self._cards[key] = card
            row2.addWidget(card, stretch=1)

        root.addLayout(row2, stretch=1)

        # 4. Bottom Timestamp Caption
        self.timestamp_lbl = QLabel("Awaiting raw-water sample analysis")
        self.timestamp_lbl.setObjectName("AnalyzedTimestamp")
        root.addWidget(self.timestamp_lbl)

    def set_state(self, state: str, data: dict | None = None) -> None:
        if state == "idle":
            self.sample_id_lbl.setText("Waiting for analysis")
            self.status_lbl.setText("Status: Ready")
            self.timestamp_lbl.setText("Awaiting raw-water sample analysis")
            for card in self._cards.values():
                card.set_value(None)

        elif state == "analyzing":
            self.sample_id_lbl.setText("Pending...")
            self.status_lbl.setText("Status: Analyzing Sample...")
            self.timestamp_lbl.setText("Reading sensors and running ML inference...")

        elif state == "complete" and data:
            self.sample_id_lbl.setText(data.get("sample_ref_number", "--"))
            self.status_lbl.setText("Status: Analysis Complete")

            wq = data.get("raw_water_quality", {})
            for key, card in self._cards.items():
                card.set_value(wq.get(key))

            raw_ts = data.get("analyzed_at")
            if raw_ts:
                dt = datetime.fromisoformat(raw_ts)
                self.timestamp_lbl.setText(f"Analyzed {dt.strftime('%d %b %Y, %H:%M UTC')}")
            else:
                self.timestamp_lbl.setText("Analysis complete")