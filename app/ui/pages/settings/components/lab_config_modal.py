from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QDoubleValidator, QIntValidator


class SequenceInputRow(QFrame):
    """Represents one dynamic row in the Slow Mixing Sequence list."""
    remove_requested = Signal(object)

    def __init__(self, seq_no: int, parent=None):
        super().__init__(parent)
        self.setObjectName("ModalSequenceRow")
        self.seq_no = seq_no

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(10)

        self.badge = QLabel(f"Seq {seq_no}")
        self.badge.setObjectName("SeqBadge")
        self.badge.setFixedWidth(48)

        self.rpm_input = QLineEdit()
        self.rpm_input.setPlaceholderText("RPM")
        self.rpm_input.setValidator(QIntValidator(1, 5000))

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("Duration (sec)")
        self.duration_input.setValidator(QIntValidator(1, 86400))

        remove_btn = QPushButton("✕")
        remove_btn.setObjectName("RemoveSeqBtn")
        remove_btn.setFixedSize(28, 28)
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.clicked.connect(lambda: self.remove_requested.emit(self))

        layout.addWidget(self.badge)
        layout.addWidget(self.rpm_input)
        layout.addWidget(self.duration_input)
        layout.addWidget(remove_btn)

    def set_sequence_number(self, seq_no: int) -> None:
        self.seq_no = seq_no
        self.badge.setText(f"Seq {seq_no}")


class LabConfigModal(QDialog):
    configuration_saved = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create Lab Configuration")
        self.setModal(True)
        self.resize(680, 520)
        self.setObjectName("LabConfigModal")

        self._sequence_rows: list[SequenceInputRow] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Scrollable Body
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        body = QWidget()
        body.setObjectName("ModalBody")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(20, 16, 20, 16)
        body_layout.setSpacing(16)

        # profile container
        self.profile_frame = QFrame()
        self.profile_frame.setObjectName('ProfileInputContainer')
        profile_container = QVBoxLayout(self.profile_frame)

        # Error Alert Banner (hidden by default)
        self.error_banner = QLabel()
        self.error_banner.setObjectName("ModalErrorBanner")
        self.error_banner.setWordWrap(True)
        self.error_banner.hide()
        profile_container.addWidget(self.error_banner)

        # 0. Profile / Operator Name
        profile_container.addWidget(self._section_heading("General Information"))
        self.name_input = self._labeled_input(
            profile_container, "Configuration / Operator Name", "e.g. Maynilad Standard Validation Procedure", is_text=True
        )

        body_layout.addWidget(self.profile_frame)

        self.analysis_frame = QFrame()
        self.analysis_frame.setObjectName("AnalysisInputContainer")
        analysis_container = QVBoxLayout(self.analysis_frame)

        # 1. Analysis Configuration
        analysis_container.addWidget(self._section_heading("Analysis Configuration"))
        analysis_grid = QGridLayout()
        analysis_grid.setSpacing(12)
        self.stirring_speed_input = self._grid_input(analysis_grid, 0, 0, "Stirring Speed (RPM)")
        self.stirring_dur_input = self._grid_input(analysis_grid, 0, 1, "Stirring Duration (sec)")
        analysis_container.addLayout(analysis_grid)

        body_layout.addWidget(self.analysis_frame)

        # 2. Coagulation Process
        self.coagulation_frame = QFrame()
        self.coagulation_frame.setObjectName('CoagulationInputContainer')
        coagulation_container = QVBoxLayout(self.coagulation_frame)

        coagulation_container.addWidget(self._section_heading("Coagulation Process"))

        flash_box = QFrame()
        flash_box.setObjectName("ModalSubBox")
        flash_layout = QVBoxLayout(flash_box)
        flash_layout.setContentsMargins(14, 12, 14, 12)
        flash_title = QLabel("Flash Mixing Phase")
        flash_title.setObjectName("ModalSubTitle")
        flash_layout.addWidget(flash_title)

        flash_grid = QGridLayout()
        flash_grid.setSpacing(10)
        self.flash_speed_input = self._grid_input(flash_grid, 0, 0, "Speed (RPM)")
        self.flash_dur_input = self._grid_input(flash_grid, 0, 1, "Duration (sec)")
        self.dispense_timing_input = self._grid_input(flash_grid, 0, 2, "Dispense Timing (sec)")
        flash_layout.addLayout(flash_grid)
        coagulation_container.addWidget(flash_box)

        # Slow Mixing Sequence Header + Add Button

        slow_box = QFrame()
        slow_box.setObjectName("ModalSubBox")

        slow_layout = QVBoxLayout(slow_box)
        slow_layout.setContentsMargins(14, 12, 14, 12)
        slow_layout.setSpacing(10)

        # Header + Add Button
        seq_header = QHBoxLayout()

        seq_title = QLabel("Slow Mixing Sequence")
        seq_title.setObjectName("ModalSubTitle")

        add_seq_btn = QPushButton("+ Add Sequence")
        add_seq_btn.setObjectName("AddSequenceBtn")
        add_seq_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_seq_btn.clicked.connect(self._add_sequence)

        seq_header.addWidget(seq_title)
        seq_header.addStretch()
        seq_header.addWidget(add_seq_btn)

        slow_layout.addLayout(seq_header)

        # Empty Sequence Placeholder
        self.empty_seq_label = QLabel("No sequences added. Click '+ Add Sequence' to begin.")
        self.empty_seq_label.setObjectName("EmptySeqPlaceholder")
        self.empty_seq_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        slow_layout.addWidget(self.empty_seq_label)

        # Sequences Container
        self.sequences_container = QVBoxLayout()
        self.sequences_container.setSpacing(8)

        slow_layout.addLayout(self.sequences_container)

        # Add Slow Mixing Box to Main Container
        coagulation_container.addWidget(slow_box)

        # Settling Phase
    
        settling_box = QFrame()
        settling_box.setObjectName("ModalSubBox")

        settling_layout = QVBoxLayout(settling_box)
        settling_layout.setContentsMargins(14, 12, 14, 12)
        settling_layout.setSpacing(10)

        settling_title = QLabel("Settling Phase")
        settling_title.setObjectName("ModalSubTitle")
        settling_layout.addWidget(settling_title)
        settling_grid = QGridLayout()
        self.settling_dur_input = self._grid_input(settling_grid, 0, 0, "Settling Time (sec)")
        settling_grid.setColumnStretch(1, 1)
        settling_layout.addLayout(settling_grid)

        coagulation_container.addWidget(settling_box)

        body_layout.addWidget(self.coagulation_frame)

        # 3. Stock Solution Configuration
        self.stock_frame = QFrame()
        self.stock_frame.setObjectName("StockInputContainer")
        stock_container = QVBoxLayout(self.stock_frame)

        stock_container.addWidget(self._section_heading("Stock Solution Configuration"))
        stock_grid = QGridLayout()
        stock_grid.setSpacing(12)
        self.sample_vol_input = self._grid_input(stock_grid, 0, 0, "Sample Volume (L)", allow_decimal=True)
        self.stock_conc_input = self._grid_input(stock_grid, 0, 1, "Stock Concentration (g/L)", allow_decimal=True)
        stock_container.addLayout(stock_grid)
        body_layout.addWidget(self.stock_frame)

        body_layout.addStretch()
        scroll.setWidget(body)
        root.addWidget(scroll)

        # Modal Footer
        footer = QFrame()
        footer.setObjectName("ModalFooter")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 12, 20, 12)
        

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("ModalCancelBtn")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save Configuration")
        save_btn.setObjectName("ModalSaveBtn")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._handle_submit)

        footer_layout.addWidget(cancel_btn)
        footer_layout.addWidget(save_btn)
        root.addWidget(footer)

    def _section_heading(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("ModalSectionHeading")
        return lbl

    def _labeled_input(self, parent_layout: QVBoxLayout, label_text: str, placeholder: str = "", is_text: bool = False) -> QLineEdit:
        wrapper = QVBoxLayout()
        wrapper.setSpacing(4)
        lbl = QLabel(label_text)
        lbl.setObjectName("InputLabel")
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        if not is_text:
            inp.setValidator(QIntValidator(0, 100000))
        wrapper.addWidget(lbl)  
        wrapper.addWidget(inp)
        parent_layout.addLayout(wrapper)
        return inp

    def _grid_input(self, grid: QGridLayout, row: int, col: int, label_text: str, allow_decimal: bool = False) -> QLineEdit:
        container = QWidget()
        v_layout = QVBoxLayout(container)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.setSpacing(4)

        lbl = QLabel(label_text)
        lbl.setObjectName("InputLabel")
        inp = QLineEdit()
        inp.setValidator(QDoubleValidator(0.0, 100000.0, 4) if allow_decimal else QIntValidator(0, 100000))

        v_layout.addWidget(lbl)
        v_layout.addWidget(inp)
        grid.addWidget(container, row, col)
        return inp

    def _add_sequence(self) -> None:
        self.empty_seq_label.hide()
        row = SequenceInputRow(len(self._sequence_rows) + 1)
        row.remove_requested.connect(self._remove_sequence)
        self._sequence_rows.append(row)
        self.sequences_container.addWidget(row)

    def _remove_sequence(self, row_widget: SequenceInputRow) -> None:
        self._sequence_rows.remove(row_widget)
        row_widget.deleteLater()
        for idx, row in enumerate(self._sequence_rows):
            row.set_sequence_number(idx + 1)
        if not self._sequence_rows:
            self.empty_seq_label.show()

    def _show_error(self, message: str) -> None:
        self.error_banner.setText(message)
        self.error_banner.show()

    def _handle_submit(self) -> None:
        self.error_banner.hide()

        # Validate required fields
        name = self.name_input.text().strip()
        if not name:
            self._show_error("Configuration / Operator Name is required.")
            return

        required_fields = [
            (self.stirring_speed_input, "Stirring Speed"),
            (self.stirring_dur_input, "Stirring Duration"),
            (self.flash_speed_input, "Flash Mixing Speed"),
            (self.flash_dur_input, "Flash Mixing Duration"),
            (self.dispense_timing_input, "Dispense Timing"),
            (self.settling_dur_input, "Settling Duration"),
            (self.sample_vol_input, "Sample Volume"),
            (self.stock_conc_input, "Stock Concentration"),
        ]
        for field, label in required_fields:
            if not field.text().strip():
                self._show_error(f"{label} is required.")
                return

        flash_duration = int(self.flash_dur_input.text())
        dispense_timing = int(self.dispense_timing_input.text())

        # Fail-safe validation rule from your React code
        if dispense_timing >= flash_duration:
            self._show_error(
                f"Dispense timing ({dispense_timing}s) cannot be equal to or greater than the flash mixing duration ({flash_duration}s)."
            )
            return

        sequences_payload = []
        for idx, row in enumerate(self._sequence_rows):
            if not row.rpm_input.text().strip() or not row.duration_input.text().strip():
                self._show_error(f"Please fill in both RPM and Duration for Seq {idx + 1}.")
                return
            sequences_payload.append({
                "sequence_no": idx + 1,
                "rpm": int(row.rpm_input.text()),
                "duration": int(row.duration_input.text()),
            })

        # Exact payload structure expected by your service layer
        payload = {
            "name": name,
            "is_active": True,
            "coagulation_config": {
                "flash_mixing_speed": int(self.flash_speed_input.text()),
                "flash_mixing_duration": flash_duration,
                "coagulant_dispense_timing": dispense_timing,
                "slow_mixing_configurations": sequences_payload,
                "settling_duration": int(self.settling_dur_input.text()),
            },
            "concentration_config": {
                "sample_volume": float(self.sample_vol_input.text()) if "." in self.sample_vol_input.text() else int(self.sample_vol_input.text()),
                "stock_concentration": float(self.stock_conc_input.text()) if "." in self.stock_conc_input.text() else int(self.stock_conc_input.text()),
            },
            "analysis_config": {
                "stirring_speed": int(self.stirring_speed_input.text()),
                "stirring_duration": int(self.stirring_dur_input.text()),
            },
        }

        self.configuration_saved.emit(payload)
        self.accept()