from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QMessageBox,
    QHeaderView,
    QGridLayout,
    QScrollArea,
    QFrame,
    QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap



class CatalogueView(QWidget):

    def __init__(self, movie_ctrl, user,on_deconnecter_callback):
        super().__init__()

        self.movie_ctrl = movie_ctrl
        self.user = user
        self.on_deconnecter_callback = on_deconnecter_callback

        self.setWindowTitle("Catalogue")
        self.resize(700, 500)

        self.setup_ui()
        self.charger_films()
        

    def setup_ui(self):

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        btn_layout = QHBoxLayout() 
        deconnecter_button = QPushButton("Se déconnecter")
        deconnecter_button.clicked.connect(self.on_deconnecter)
        
        deconnecter_button.setStyleSheet("""
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
        """)
        # Titre
        self.title_label = QLabel(" Catalogue")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: gray;
            margin-bottom: 10px;
            border-bottom: 2px solid #730101;
        """)

        # Utilisateur connecté
        self.user_label = QLabel(
            f"Utilisateur connecté : {self.user.name}"
        )
        self.user_label = QLabel(f"Utilisateur connecté : {self.user.name}")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setStyleSheet("color: gray; font-size: 13px;border-bottom:1px solid #730101 ")
        
        # liste films
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.movies_container = QWidget()
        self.movies_layout =  QGridLayout()   # ou QGridLayout si tu veux mieux

        self.movies_container.setLayout(self.movies_layout)

        self.scroll.setWidget(self.movies_container)
        self.scroll.setStyleSheet("border-bottom:1px solide #730101")

        
        # Zone note
        note_layout = QHBoxLayout()

        self.score_input = QSpinBox()
        self.score_input.setMinimum(1)
        self.score_input.setMaximum(5)
        self.score_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                color: gray;
                border: 2px solid #444;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)

        self.note_button = QPushButton(" Noter")
        self.history_button = QPushButton("📋 Mon historique")

        # Connexion boutons
        self.note_button.clicked.connect(self.on_noter)
        self.history_button.clicked.connect(self.on_historique)
        btn_style = """
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
        self.note_button.setStyleSheet(btn_style)
        self.history_button.setStyleSheet(btn_style)

        # Ajouter éléments zone note
        note_layout.addWidget(QLabel("Note :"))
        note_layout.addWidget(self.score_input)
        note_layout.addWidget(self.note_button)
        note_layout.addWidget(self.history_button)

        # Ajouter widgets au layout principal
        layout.addWidget(self.title_label)
        layout.addWidget(deconnecter_button)
        layout.addWidget(self.user_label)
        layout.addWidget(self.scroll)
        layout.addLayout(note_layout)

        self.setLayout(layout)

    
    def charger_films(self):

        films = self.movie_ctrl.get_catalogue()

        # vider layout
        for i in reversed(range(self.movies_layout.count())):
            item = self.movies_layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        columns = 4   # nombre de films par ligne

        for index, movie in enumerate(films):
            # IMAGE
            image_label = QLabel()
            image_label.setFixedSize(180, 280)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setCursor(Qt.PointingHandCursor)

            image_path = movie.image if hasattr(movie, 'image') else ""
            pixmap = QPixmap(image_path)

            if pixmap.isNull():
                # Image introuvable → icône selon genre
                genres_icons = {
                    "Historical": "🏰", "Crime": "🔍",
                    "Drama": "🎭",      "Romance": "❤️",
                    "Action": "⚡",     "Sci-Fi": "🚀",
                    "Thriller": "😱",   "Horror": "👻",
                    "Comedy": "😂",
                }
                image_label.setText(genres_icons.get(movie.genre, "🎬"))
                image_label.setStyleSheet("""
                    font-size: 50px;
                    background-color: #222;
                    border-radius: 12px;
                """)
            else:
                image_label.setPixmap(
                    pixmap.scaled(image_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                )
                image_label.setStyleSheet("border-radius: 12px;")
                image_label.setPixmap(pixmap.scaled(image_label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
                image_label.setScaledContents(True)            

            

            # CLIC sur la carte → sélectionne le film
            image_label.mousePressEvent = lambda event, m=movie: self.selectionner_film(m)

            
            

            row = index // columns
            col = index % columns

            self.movies_layout.addWidget(image_label, row, col)

    def selectionner_film(self, movie):
        self.selected_movie = movie
        self.title_label.setText(f"  {movie.title}")

    def on_noter(self):

        if not hasattr(self, 'selected_movie') or self.selected_movie is None:
            QMessageBox.warning(self, "Erreur", "Cliquez d'abord sur une carte.")
            return

        score  = self.score_input.value()
        result = self.movie_ctrl.noter_film(
            self.user,
            self.selected_movie.id,
            score
        )

        if result is None:
            QMessageBox.warning(self, "Erreur", "Film introuvable.")
        elif result == "deja_note":
            QMessageBox.warning(self, "Erreur", "Vous avez déjà noté ce film.")
        else:
            QMessageBox.information(self, "Succès", f"'{self.selected_movie.title}' noté {score}/5 ⭐")
            self.title_label.setText(" Catalogue")
            self.selected_movie = None
                

    def on_historique(self):

        historique = self.movie_ctrl.get_historique(
            self.user
        )

        if not historique:
            texte = "Aucun film noté"
        else:
            texte = ""

            for rating in historique:
                texte += (
                    f"{rating.movie.title} "
                    f"- Note : {rating.score}/5\n"
                )

        QMessageBox.information(
            self,
            "Historique",
            texte
        )
    #retoure a la page de login
    def on_deconnecter(self):
        self.on_deconnecter_callback()