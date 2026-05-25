import mysql.connector

class Database:
    def __init__(self):
        self.movies = []
        self.users = []
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",       
            database="recommendation_film"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    def load_data(self):
        from models.Movie import Movie
        from models.User import User

        # Charger les films
        self.cursor.execute("SELECT * FROM movies")
        for row in self.cursor.fetchall():
            self.movies.append(Movie(row['id'], row['title'], row['genre'], row['year'],row['image'],row.get('description','')))

        # Charger les utilisateurs
        self.cursor.execute("SELECT * FROM users")
        for row in self.cursor.fetchall():
            
            new_user = User( row['name'], row['email'], str(row['id']))

            # Charger les ratings de cet utilisateur
            self.cursor.execute(
                "SELECT * FROM ratings WHERE user_id = %s", (row['id'],)
            )
            for r in self.cursor.fetchall():
                movie = self.find_movie(r['movie_id'])
                if movie:
                    new_user.rate_movie(movie, r['score'])

            self.users.append(new_user)

    def save_user(self, user):
        self.cursor.execute(
            "INSERT IGNORE INTO users (name, email) VALUES ( %s, %s)",
            (user.name, user.email)
        )
        self.conn.commit()

    def save_rating(self, user, movie, score):
        self.cursor.execute(
            "INSERT INTO ratings (user_id, movie_id, score) VALUES (%s, %s, %s)",
            (user.id, movie.id, score)
        )
        self.conn.commit()

    def save_data(self):
        # Sauvegarder les films
        for m in self.movies:
            self.cursor.execute(
                "INSERT IGNORE INTO movies (id, title, genre, year) VALUES (%s, %s, %s, %s)",
                (m.id, m.title, m.genre, m.year)
            )
        # Sauvegarder les utilisateurs
        for u in self.users:
            self.cursor.execute(
                "INSERT IGNORE INTO users ( name, email) VALUES ( %s, %s)",
                ( u.name, u.email)
            )
            for r in u.ratings:
                self.cursor.execute(
                    "INSERT IGNORE INTO ratings (user_id, movie_id, score) VALUES (%s, %s, %s)",
                    (u.id, r.movie.id, r.score)
                )
        self.conn.commit()

    def find_user(self, user_id):
        for u in self.users:
            if u.id == str(user_id):
                return u
        return None

    def find_movie(self, movie_id):
        for m in self.movies:
            if m.id == movie_id:
                return m
        return None

    def close(self):
        self.cursor.close()
        self.conn.close()