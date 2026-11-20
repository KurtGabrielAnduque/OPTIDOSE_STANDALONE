from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class KpiMetricBox(QFrame):
    def __init__(self, title: str, value: str | int | float, unit: str, large: bool = True, parent=None):
        super().__init__(parent)
        self.setObjectName("KpiMetricBox")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        self.title_lbl = QLabel(title.upper())
        self.title_lbl.setObjectName("KpiCaption")

        value_row = QHBoxLayout()
        value_row.setContentsMargins(0, 0, 0, 0)
        value_row.setSpacing(5)

        self.value_lbl = QLabel(str(value))
        self.value_lbl.setObjectName("KpiValueLarge" if large else "KpiValueMedium")

        self.unit_lbl = QLabel(unit)
        self.unit_lbl.setObjectName("KpiUnit")
        self.unit_lbl.setAlignment(Qt.AlignmentFlag.AlignBottom)

        value_row.addWidget(self.value_lbl)
        value_row.addWidget(self.unit_lbl)
        value_row.addStretch()

        layout.addWidget(self.title_lbl)
        layout.addLayout(value_row)