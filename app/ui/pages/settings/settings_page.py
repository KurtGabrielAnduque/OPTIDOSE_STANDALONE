from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
)


from app.ui.pages.settings.components.lab_config_modal import LabConfigModal
from app.ui.pages.settings.components.lab_settings_display import LabSettingsDisplay


class SettingsPage(QFrame):
    # Signal you will connect to your service layer later
    settings_submitted = Signal(dict)

    def __init__(self, active_settings: dict | None = None):
        super().__init__()
        self.setObjectName("SettingsFrame")
        self._active_settings = active_settings

        self._load_style()
        self._setup_ui()

    def _load_style(self) -> None:
        qss_path = Path(__file__).parent / "styles" / "settings_page_style.qss"
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def _setup_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 10)
        root_layout.setSpacing(0)

        # Sticky Top Header
        root_layout.addWidget(self._build_header())

        # Body Area (switches between Empty State and Display State)
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("SettingsScroll")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self.empty_state_widget = self._build_empty_state()
        self.display_widget = LabSettingsDisplay(self._active_settings) if self._active_settings else None

        root_layout.addWidget(self.scroll_area)
        root_layout.addWidget(self.empty_state_widget)

        self._refresh_view()

    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("MainLabelFrame")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 14, 20, 14)

        # Left Title + Active Badge
        left_col = QVBoxLayout()
        left_col.setSpacing(3)

        title_row = QHBoxLayout()
        title_row.setSpacing(10)
        title = QLabel("Lab Settings")
        title.setObjectName("PageTitle")


        title_row.addWidget(title)
        title_row.addStretch()

        subtitle = QLabel("Overall configuration of the OPTIDOSE system")
        subtitle.setObjectName("PageSubtitle")

        left_col.addLayout(title_row)
        left_col.addWidget(subtitle)

        # Right Operator Name + Created Date + Create Button
        right_col = QVBoxLayout()
        right_col.setSpacing(2)
        right_col.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.operator_lbl = QLabel()
        self.operator_lbl.setObjectName("OperatorNameLabel")
        self.operator_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.date_lbl = QLabel()
        self.date_lbl.setObjectName("DateCreatedLabel")
        self.date_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)

        right_col.addWidget(self.operator_lbl)
        right_col.addWidget(self.date_lbl)

        self.create_btn = QPushButton("+ New Configuration")
        self.create_btn.setObjectName("PrimaryActionBtn")
        self.create_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.create_btn.setFixedHeight(36)
        self.create_btn.clicked.connect(self._open_create_modal)

        layout.addLayout(left_col)
        layout.addStretch()
        layout.addLayout(right_col)
        layout.addSpacing(14)
        layout.addWidget(self.create_btn)

        return header

    def _build_empty_state(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("EmptyStateFrame")
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        heading = QLabel("No Active Configuration Found")
        heading.setObjectName("EmptyHeading")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        desc = QLabel(
            "There are currently no active lab configurations in the system.\n"
            "You must create one first before proceeding."
        )
        desc.setObjectName("EmptyDesc")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn = QPushButton("+ Create Configuration")
        btn.setObjectName("PrimaryActionBtn")
        btn.setFixedHeight(40)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._open_create_modal)

        layout.addWidget(heading)
        layout.addWidget(desc)
        layout.addSpacing(8)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)
        return frame

    def _refresh_view(self) -> None:
        has_config = bool(self._active_settings)
        self.operator_lbl.setVisible(has_config)
        self.date_lbl.setVisible(has_config)
        self.create_btn.setVisible(has_config)

        if has_config:
            self.operator_lbl.setText(f'Operator: {self._active_settings["name"]}')
            created_raw = self._active_settings.get("created_at")
            if created_raw:
                dt = datetime.fromisoformat(created_raw)
                self.date_lbl.setText(f"Created: {dt.strftime('%m/%d/%Y')}")
            else:
                self.date_lbl.setText(f"Created: {datetime.now().strftime('%m/%d/%Y')}")

            if self.display_widget is None:
                self.display_widget = LabSettingsDisplay(self._active_settings)
            else:
                self.display_widget.render_settings(self._active_settings)

            self.scroll_area.setWidget(self.display_widget)
            self.empty_state_widget.hide()
            self.scroll_area.show()
        else:
            self.scroll_area.hide()
            self.empty_state_widget.show()

    def _open_create_modal(self) -> None:
        modal = LabConfigModal(self)
        modal.configuration_saved.connect(self._on_configuration_saved)
        modal.exec()

    def _on_configuration_saved(self, payload: dict) -> None:
        # Emit clean payload for the service layer
        self.settings_submitted.emit(payload)

        # Update UI immediately with the newly saved config
        self._active_settings = {
            **payload,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        print(self._active_settings)
        self._refresh_view()