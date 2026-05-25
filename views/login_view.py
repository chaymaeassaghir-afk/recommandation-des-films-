from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
        QLabel, QLineEdit, QPushButton, QMessageBox, QFrame)
from PySide6.QtCore import Qt
class LoginView (QWidget):
    def __init__(self, auth_ctrl, on_login_callback):
        super().__init__()

        self.auth_ctrl = auth_ctrl
        self.on_login_callback = on_login_callback

        self.setWindowTitle("Connexion")
        self.resize(300,250)

        self.setup_ui()

    def  setup_ui(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        self.setLayout(layout)

        card = QFrame()
        card.setFixedWidth(380)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E7DFF5;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)
        card_layout.setContentsMargins(25, 25, 25, 25)

        self.titre=QLabel("🎬 CineRec")
        self.titre.setAlignment(Qt.AlignCenter)
        self.titre.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: gray;
            margin-bottom: 15px;
        """)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID utilisateur")
        self.id_input.setFixedHeight(45)
        self.nom=QLineEdit()
        self.nom.setPlaceholderText("Nom")
        self.nom.setFixedHeight(45)
        self.email=QLineEdit()
        self.email.setPlaceholderText("Email")
        self.email.setFixedHeight(45)
        
        style = """
            QLineEdit {
                background-color: #FFFFFF;
                border: 2px solid #E7DFF5;
                border-radius: 12px;
                padding-left: 15px;
                color: #4A4458;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #730101;
            }
            """
        for input in [self.id_input, self.nom, self.email]:
            input.setStyleSheet(style)

        self.login=QPushButton("Se connecter")
        

        self.login.clicked.connect(self.on_connecter)

        style = """
            QPushButton {
                background-color: #730101;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #730101;
            }
            QPushButton:hover {
                background-color: #730101;
                color: white;
            }
        """
        for btn in [self.login]:
            btn.setStyleSheet(style)    
        
        card_layout.addWidget(QLabel("Identifiant :"))
        card_layout.addWidget(self.id_input)
        card_layout.addSpacing(5)
        card_layout.addWidget(self.login)


        layout.addWidget(self.titre)
        layout.addWidget(self.id_input)
        layout.addWidget(self.nom)
        layout.addWidget(self.email)
        layout.addWidget(self.login)
        

        self.setLayout(layout)

    def on_connecter(self,):
        user_id=self.id_input.text()
        user=self.auth_ctrl.connecter(user_id)
        if user is None :
            QMessageBox.warning(
                self,
                "Erreur",
                "Utilisateur introuvable"
            )
        else:
            self.on_login_callback(user)


               