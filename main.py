import sys
from PySide6.QtWidgets import QApplication
from engine.Database import Database
from engine.RecommendationEngine import RecommendationEngine
from engine.tfidf import TFIDFEngine
from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #FFF8FA;
            color: #5F5A7A;
            font-size: 14px;
            font-family: Segoe UI;
        }

        QFrame {
            background-color: white;
            border: 1px solid #E7DFF5;
            border-radius: 18px;
        }

        QLabel {
            color: #5F5A7A;
        }

        QLineEdit, QSpinBox {
            background-color: white;
            border: 2px solid #E7DFF5;
            border-radius: 12px;
            padding: 10px;
            color: #4A4458;
            font-size: 14px;
        }

        QLineEdit:focus, QSpinBox:focus {
            border: 2px solid #D4537E;
        }

        QPushButton {
            background-color: #D4537E;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 16px;
            font-weight: bold;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #BA3D67;
        }

        QPushButton:pressed {
            background-color: #A52E58;
        }

        QTableWidget {
            background-color: white;
            border-radius: 14px;
            border: 1px solid #E7DFF5;
            gridline-color: #F0EAF7;
         
            
        }

        QHeaderView::section {
            background-color: #7F77DD;
            color: white;
            border: none;
            padding: 10px;
            font-weight: bold;
            border-radius: 0px;
            
        }

        QTableWidget::item:hover {
            background-color: #FBEAF0;
            color: #3C3489;
        
        }
        """)

    db  = Database()
    db.load_data()
    tfidf  = TFIDFEngine(db)
    engine = RecommendationEngine(db,tfidf)
    window = MainWindow(db, engine, tfidf)
    window.setWindowTitle("🎬 CineRec")
    window.setMinimumSize(900, 650)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()