from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
from app.ui.pages.settings.components.kpi_metric_box import KpiMetricBox


class LabSettingsDisplay(QFrame):
    def __init__(self, active_settings: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("SettingsDisplayContainer")

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 6, 0)
        self._layout.setSpacing(14)

        self.render_settings(active_settings)

    def render_settings(self, cfg: dict) -> None:
        # Clear previous widgets when refreshing after modal save
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._layout.addWidget(self._build_analysis_card(cfg["analysis_config"]))
        self._layout.addWidget(self._build_coagulation_card(cfg["coagulation_config"]))
        self._layout.addWidget(self._build_stock_solution_card(cfg["concentration_config"]))
        self._layout.addStretch()

    def _create_section_card(self, title: str) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setObjectName("SectionCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        header = QLabel(title)
        header.setObjectName("SectionTitle")
        layout.addWidget(header)
        return card, layout

    def _build_analysis_card(self, analysis: dict) -> QFrame:
        card, layout = self._create_section_card("Analysis Configuration")
        row = QHBoxLayout()
        row.setSpacing(12)

        row.addWidget(KpiMetricBox("Stirring Speed", analysis["stirring_speed"], "RPM", large=True))
        row.addWidget(KpiMetricBox("Stirring Duration", analysis["stirring_duration"], "sec", large=True))
        layout.addLayout(row)
        return card

    def _build_coagulation_card(self, coag: dict) -> QFrame:
        card, layout = self._create_section_card("Coagulation Process")

        # Flash Mixing Phase
        flash_lbl = QLabel("Flash Mixing Phase")
        flash_lbl.setObjectName("SubSectionTitle")
        layout.addWidget(flash_lbl)

        flash_row = QHBoxLayout()
        flash_row.setSpacing(12)
        flash_row.addWidget(KpiMetricBox("Speed", coag["flash_mixing_speed"], "RPM", large=False))
        flash_row.addWidget(KpiMetricBox("Duration", coag["flash_mixing_duration"], "sec", large=False))
        flash_row.addWidget(KpiMetricBox("Dispense Timing", coag["coagulant_dispense_timing"], "sec", large=False))
        layout.addLayout(flash_row)

        # Slow Mixing Sequence Table
        seq_lbl = QLabel("Slow Mixing Sequence")
        seq_lbl.setObjectName("SubSectionTitle")
        layout.addWidget(seq_lbl)

        sequences = coag.get("slow_mixing_configurations", [])
        table = QTableWidget(len(sequences), 3)
        table.setObjectName("SequenceTable")
        table.setHorizontalHeaderLabels(["Sequence No.", "Speed (RPM)", "Duration (sec)"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for row_idx, step in enumerate(sequences):
            table.setRowHeight(row_idx, 36)

            item1 = QTableWidgetItem(f"Sequence {step['sequence_no']}")
            item2 = QTableWidgetItem(str(step["rpm"]))
            item3 = QTableWidgetItem(str(step["duration"]))

            item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            table.setItem(row_idx, 0, item1)
            table.setItem(row_idx, 1, item2)
            table.setItem(row_idx, 2, item3)

        # Auto-fit table height to rows so it never nests scrollbars
        total_height = table.horizontalHeader().height() + (len(sequences) * 36) + 4
        table.setFixedHeight(max(total_height, 72))
        layout.addWidget(table)

        # Settling Phase
        settling_lbl = QLabel("Settling Phase")
        settling_lbl.setObjectName("SubSectionTitle")
        layout.addWidget(settling_lbl)

        settling_row = QHBoxLayout()
        settling_row.addWidget(KpiMetricBox("Duration", coag["settling_duration"], "sec", large=False))
        settling_row.addStretch()
        layout.addLayout(settling_row)

        return card

    def _build_stock_solution_card(self, conc: dict) -> QFrame:
        card, layout = self._create_section_card("Stock Solution")
        row = QHBoxLayout()
        row.setSpacing(12)

        row.addWidget(KpiMetricBox("Sample Volume", conc["sample_volume"], "L", large=True))
        row.addWidget(KpiMetricBox("Stock Concentration", conc["stock_concentration"], "g/L", large=True))
        layout.addLayout(row)
        return card