from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
        QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
class InscriptionView(QWidget):
    def __init__(self, auth_ctrl, on_login_callback):
        super().__init__()

        self.auth_ctrl = auth_ctrl
        self.on_login_callback = on_login_callback

        self.setWindowTitle("Inscription ")
        self.resize(300,250)

        self.setup_ui()

    def  setup_ui(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        self.setLayout(layout)

        

        self.titre=QLabel("🎬 CineRec")
        self.titre.setAlignment(Qt.AlignCenter)
        self.titre.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: gray;
            margin-bottom: 10px;
        """)

        self.nom=QLineEdit()
        self.nom.setPlaceholderText("Nom")

        self.email=QLineEdit()
        self.email.setPlaceholderText("Email")

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
        for input in [ self.nom, self.email]:
            input.setStyleSheet(style)

        self.inscrire=QPushButton("Creer un compte")

        self.inscrire.clicked.connect(self.on_inscrire)

        style = """
            QPushButton {
                background-color: #730101;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #730101;
                font-size: 13px;
            }  
            QPushButton:hover {
                background-color: #730101;
                color: white;
            }  
            """
        for btn in [self.inscrire]:
            btn.setStyleSheet(style)    

        layout.addWidget(self.titre)
        
        layout.addWidget(self.nom)
        layout.addWidget(self.email)
       
        layout.addWidget(self.inscrire)

        self.setLayout(layout)

   

    def on_inscrire(self):
        name = self.nom.text()
        email = self.email.text()    

        if  not name or not email:
            QMessageBox.warning(self,"Erreuer","Veuillez remplir tous les champs")
            return


        user=self.auth_ctrl.creer_compte(name,email)

        if user is None :
            QMessageBox.warning(self,"ERREUR","Impossible de creer compte")
        else:
            self.on_login_callback(user)

    def reset(self):

        
        self.nom.clear()
        self.email.clear()            