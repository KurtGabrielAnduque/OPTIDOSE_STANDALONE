from pathlib import Path
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


def create_colored_svg_icon(svg_path: Path, color_hex: str, size: int = 20) -> QIcon:
    """Renders an SVG icon in a specific solid color (for normal vs active states)."""
    if not svg_path.exists():
        return QIcon()

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    renderer = QSvgRenderer(str(svg_path))
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color_hex))
    painter.end()

    return QIcon(pixmap)


class NavigationBar(QFrame):
    page_changed = Signal(int)

    def __init__(self, navigation_page_lists: list[tuple[str, str]]):
        super().__init__()
        self.setObjectName("NavigationBar")
        self.expanded_width = 230
        self.collapsed_width = 78
        self.is_collapsed = False
        self.setFixedWidth(self.expanded_width)

        self._nav_items = navigation_page_lists
        self._buttons: list[tuple[QPushButton, str, str]] = []
        self._icons_dir = Path(__file__).resolve().parents[2] / "resources" / "images"

        self._apply_card_shadow()
        self._load_style()
        self._setup_ui()

    def _apply_card_shadow(self) -> None:
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(15, 23, 42, 22))
        self.setGraphicsEffect(shadow)

    def _load_style(self) -> None:
        qss_path = Path(__file__).parent / "styles" / "navigation_bar.qss"
        if qss_path.exists():
            self.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    def _setup_ui(self) -> None:
        navigation_layout = QVBoxLayout(self)
        navigation_layout.setContentsMargins(14, 20, 14, 20)
        navigation_layout.setSpacing(6)

        # Header Row: [☰] [OPTIDOSE]
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(6, 0, 6, 14)
        header_layout.setSpacing(12)

        self.toggle_btn = QPushButton("☰")
        self.toggle_btn.setObjectName("MenuToggleButton")
        self.toggle_btn.setFixedSize(32, 32)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)

        self.nav_label = QLabel("OPTIDOSE")
        self.nav_label.setObjectName("main-label")

        header_layout.addWidget(self.toggle_btn)
        header_layout.addWidget(self.nav_label)
        header_layout.addStretch()

        navigation_layout.addLayout(header_layout)

        # Navigation Buttons
        self.group_buttons = QButtonGroup(self)
        self.group_buttons.setExclusive(True)
        self.group_buttons.idClicked.connect(self._on_button_clicked)

        for index, (label, icon_file) in enumerate(self._nav_items):
            if label == "Settings":
                navigation_layout.addStretch()
                separator = QFrame()
                separator.setObjectName("SettingsSeparator")
                separator.setFixedHeight(2)
                navigation_layout.addWidget(separator)

            button = QPushButton(f" {label}")
            button.setObjectName("NavButton")
            button.setCheckable(True)
            button.setFixedHeight(44)
            button.setIconSize(QSize(19, 19))
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            if index == 0:
                button.setChecked(True)

            navigation_layout.addWidget(button)
            self.group_buttons.addButton(button, index)
            self._buttons.append((button, label, icon_file))

        self._refresh_button_icons()

    def _on_button_clicked(self, index: int) -> None:
        self._refresh_button_icons()
        self.page_changed.emit(index)

    def _refresh_button_icons(self) -> None:
        for button, _, icon_file in self._buttons:
            svg_path = self._icons_dir / icon_file
            color = "#FFFFFF" if button.isChecked() else "#6B7280"
            button.setIcon(create_colored_svg_icon(svg_path, color, size=20))

    def toggle_sidebar(self) -> None:
        self.is_collapsed = not self.is_collapsed
        if self.is_collapsed:
            self.setFixedWidth(self.collapsed_width)
            self.nav_label.hide()
            for button, label, _ in self._buttons:
                button.setText("")
                button.setToolTip(label)
        else:
            self.setFixedWidth(self.expanded_width)
            self.nav_label.show()
            for button, label, _ in self._buttons:
                button.setText(f"  {label}")
                button.setToolTip("")