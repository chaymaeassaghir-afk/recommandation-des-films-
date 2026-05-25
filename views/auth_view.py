from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,QPushButton, QStackedWidget)

class AuthView(QWidget):
    def __init__(self, auth_ctrl, on_login_callback):
        super().__init__()
        self.auth_ctrl = auth_ctrl
        self.on_login_callback = on_login_callback
        self.setup_ui()

    def setup_ui(self):
        from views.login_view import LoginView
        from views.inscription_view import InscriptionView

        layout = QVBoxLayout()
        self.stack = QStackedWidget()

        

        self.login_view = LoginView(self.auth_ctrl, self.on_login_callback)
        self.inscription_view = InscriptionView(self.auth_ctrl, self.on_login_callback)

        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.inscription_view)

        # Boutons pour switcher
        btn_login = QPushButton("Déjà un compte ? Se connecter")
        btn_login.clicked.connect(lambda: self.stack.setCurrentWidget(self.login_view))

        btn_inscription = QPushButton("Nouveau ? Créer un compte")
        btn_inscription.clicked.connect(lambda: self.stack.setCurrentWidget(self.inscription_view))

        style = """
            QPushButton {
                background-color: #a56e6e;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #730101;
            }
            QPushButton:hover {
                background-color: #a56e6e;
                color: white;
            }
        """
        for btn in [btn_login, btn_inscription]:
            btn.setStyleSheet(style)    

        layout.addWidget(self.stack)
        layout.addWidget(btn_login)
        layout.addWidget(btn_inscription)
        self.setLayout(layout)

        

    def reset(self):
        self.login_view.reset()
        self.inscription_view.reset()

    
    