from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QTabWidget
)

from controller.auth_controller import authController
from controller.movie_controller import movieController

from views.login_view import LoginView
from views.catalogue_view import CatalogueView
from views.auth_view import AuthView
from views.recommandation_view import RecommandationView


class MainWindow(QMainWindow):

    def __init__(self, db, engine, tfidf):
        super().__init__()

        self.setWindowTitle("🎬 CineRec")
        self.resize(900, 600)

        # Controllers
        self.auth_ctrl = authController(db)

        self.movie_ctrl = movieController(
            db,
            engine,
            tfidf
        )

        # Stack principal
        self.stack = QStackedWidget()

        self.setCentralWidget(self.stack)

        # Login view
        self.auth_view = AuthView(
            self.auth_ctrl,
            self.on_login
        )

        self.stack.addWidget(self.auth_view)

    def setup_style(self):
        # Colle ce style dans main_window.py → setup_style()
        self.setStyleSheet( 
            """
            QWidget { 
                background-color: #F8F6FF;
                color: #3C3489;
                font-family: Arial;
                font-size: 13px;
            } 
            QPushButton {
                background-color: #a7a3d8;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #c7c2ff; }

            QLineEdit {
                background-color: #a56e6e;
                border: 2px solid #730101;
                border-radius: 8px;
                padding: 8px;
                color: #3C3489;
            }
            QLineEdit:focus { border: 2px solid #7F77DD; }

            QTableWidget {
                background-color: white;
                border: 0.5px solid #730101;
                border-radius: 10px;
                color: #3C3489;
                
            }
            QHeaderView::section {
                background-color: #EEEDFE;
                color: #534AB7;
                font-weight: bold;
                border: none;
                padding: 8px;
            }
            QTabBar::tab {
                background-color: #EEEDFE;
                color: #AFA9EC;
                padding: 10px 25px;
                border: none;
            }
            QTabBar::tab:selected {
                background-color: #7F77DD;
                color: white;
                font-weight: bold;
            }
        """)  

    def on_login(self, user):

        # Catalogue
        self.catalogue_view = CatalogueView(
            self.movie_ctrl,
            user,
            self.on_logout
        )

        # Recommandations
        self.recommandation_view = RecommandationView(
            self.movie_ctrl,
            user
        )

        # Tabs
        self.tabs = QTabWidget()

        self.tabs.addTab(
            self.catalogue_view,
            " Catalogue"
        )

        

        self.tabs.addTab(
            self.recommandation_view,
            " Recommandations"
        )
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background-color: #a56e6e;
                color: #fff;
                padding: 10px 25px;
                border: 2px solid #730101;
            }
            QTabBar::tab:selected {
                background-color: #7F77DD;
                color: white;
                font-weight: bold;""")
        

        # Ajouter au stack
        self.stack.addWidget(self.tabs)

        # Afficher tabs
        self.stack.setCurrentWidget(self.tabs)

    def on_logout(self):

        # Retour login
        self.stack.setCurrentWidget(
            self.auth_view
        )

        # Reset champs
        self.auth_view.reset()