from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from app.ui.pages import (
    DashBoardPage,
    DosageRecommendationPage,
    HistoryPage,
    SettingsPage,
    TreatmentPage,
)
from app.ui.components.navigation_bar import NavigationBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OptiDose")
        self.resize(1024, 600)
        self.setMinimumSize(800, 500)

        main_container = QWidget()
        main_container.setObjectName("MainContainer")
        self.setCentralWidget(main_container)

        main_layout = QHBoxLayout(main_container)
        # Outer margin lets the white sidebar card float on the soft blue background
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(14)

        # Setup all pages
        self.dashboard = DashBoardPage()
        self.dosage_recommendation = DosageRecommendationPage()
        self.treatment = TreatmentPage()
        self.history = HistoryPage()
        self.settings = SettingsPage()

        # (Label, Icon filename in app/resources/images/, Page instance)
        nav_routes = [
            ("Dashboard", "dashboard.svg", self.dashboard),
            ("Dosage Prediction", "dosage.svg", self.dosage_recommendation),
            ("Treatment Assessment", "treatment.svg", self.treatment),
            ("History", "history.svg", self.history),
            ("Settings", "settings.svg", self.settings),
        ]

        nav_items = [(label, icon) for label, icon, _ in nav_routes]
        self.navigation_bar = NavigationBar(nav_items)

        self.pages = QStackedWidget()
        self.pages.setObjectName("PageStack")
        for _, _, page in nav_routes:
            self.pages.addWidget(page)

        self.navigation_bar.page_changed.connect(self.pages.setCurrentIndex)

        main_layout.addWidget(self.navigation_bar)
        main_layout.addWidget(self.pages)