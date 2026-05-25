from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QHeaderView,
    QGridLayout,
    QScrollArea,
    QFrame,
    QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


class RecommandationView(QWidget):

    def __init__(self, movie_ctrl, user):
        super().__init__()

        self.movie_ctrl = movie_ctrl
        self.user = user

        self.setWindowTitle("Recommandations")
        self.resize(700, 500)

        self.setup_ui()

    def setup_ui(self):

        # Layout principal
        layout = QVBoxLayout()

        # Titre
        self.title_label = QLabel(" Recommandations")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: gray;
            margin-bottom: 10px;
        """)

        # Boutons recommandations
        buttons_layout = QHBoxLayout()

        btn_recs = QPushButton(" Mes recommandations")
        btn_recs.clicked.connect(self.on_recommander)
        btn_recs.setStyleSheet("""
            QPushButton {
                background-color: #730101;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color:#730101;
            }
        """)


        # Zone genre
        genre_layout = QHBoxLayout()

        self.genre_box = QComboBox()

        # Genres exemples
        genres = [
            "Action",
            "Comedy",
            "Drama",
            "Sci-Fi",
            "Romance",
            "Horror"
        ]
        self.genre_box.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: gray;
                border: 2px solid #444;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)

        self.genre_box.addItems(genres)

        self.genre_button = QPushButton("🎭 Par genre")

        self.genre_button.clicked.connect(self.on_genre)
        self.genre_button.setStyleSheet("""
            QPushButton {
                background-color: #a56e6e;
                color: white;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
                border: 1px solid #730101;
                font-size: 13px;}""")

        genre_layout.addWidget(self.genre_box)
        genre_layout.addWidget(self.genre_button)

        

        # Zone scrollable
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Container des films
        self.movies_container = QWidget()

        # Layout grille
        self.movies_layout = QGridLayout()
        self.movies_layout.setSpacing(20)

        self.movies_container.setLayout(self.movies_layout)

        self.scroll.setWidget(self.movies_container)

        

        # Ajouter éléments au layout principal
        layout.addWidget(self.title_label)
        buttons_layout.addWidget(btn_recs)
        layout.addLayout(buttons_layout)

        layout.addLayout(genre_layout)
        layout.addWidget(self.scroll)

        self.setLayout(layout)

    def afficher_resultats(self, recs):

        # vider la grille
        for i in reversed(range(self.movies_layout.count())):

            item = self.movies_layout.itemAt(i)

            if item.widget():
                item.widget().deleteLater()

        # aucun résultat
        if not recs:

            QMessageBox.information(
                self,
                "Recommandations",
                "Aucune recommandation"
            )

            return

        columns = 4

        for index, movie in enumerate(recs):

            image_label = QLabel()

            image_label.setFixedSize(180, 260)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setCursor(Qt.PointingHandCursor)

            pixmap = QPixmap(movie.image)

            if not pixmap.isNull():

                scaled_pixmap = pixmap.scaled(
                    image_label.size(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )

                image_label.setPixmap(scaled_pixmap)
                image_label.setScaledContents(True)

            else:

                image_label.setText("🎬")

                image_label.setStyleSheet("""
                    background-color: #222;
                    color: white;
                    font-size: 50px;
                    border-radius: 12px;
                """)

            # effet hover
            image_label.setStyleSheet("""
                QLabel {
                    border-radius: 12px;
                }

                QLabel:hover {
                    border: 3px solid #FBEAF0;
                }
            """)

            # clic
            image_label.mousePressEvent = (
                lambda event, m=movie: self.afficher_details(m)
            )

            row = index // columns
            col = index % columns

            self.movies_layout.addWidget(image_label, row, col)

    def afficher_details(self, movie):

            QMessageBox.information(
                self,
                movie.title,
                f"""
        Titre : {movie.title}

        Genre : {movie.genre}

        Année : {movie.year}
        """
            )

    def on_recommander(self):
        recs = self.movie_ctrl.get_recommandations(self.user)
        self.afficher_resultats(recs)

    def on_genre(self):
        genre = self.genre_box.currentText()
        recs  = self.movie_ctrl.get_recommandations_genre(self.user, genre)
        self.afficher_resultats(recs)