from sklearn.feature_extraction.text import TfidfVectorizer #transforme les textes en chiffres
from sklearn.metrics.pairwise import cosine_similarity #compare deux vecteurs de chiffres
import numpy as np #manipule les tableaux de chiffres

class TFIDFEngine:
    def __init__(self, db):
        self.db = db
        self.vectorizer = TfidfVectorizer() #l'outil qui va transformer les textes
        self.tfidf_matrix = None #le tableau de chiffres
        self.movie_ids = [] #liste des IDs des films dans le même ordre que la matrice
        self.train() #appelé automatiquement dès la création de l'objet

    def train(self):
        # Combine genre + description pour chaque film
        corpus = []
        for movie in self.db.movies:
            texte = f"{movie.genre} {movie.genre} {movie.description}"
            corpus.append(texte)
            self.movie_ids.append(movie.id)

        # Construit la matrice TF-IDF
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus) #fit_transform: fit → apprend tous les mots du corpus ,transform → convertit chaque phrase en vecteur de chiffres
        print(f" Matrice TF-IDF construite : {self.tfidf_matrix.shape}")

    def get_similar_movies(self, movie, n=8):
        if movie.id not in self.movie_ids:
            return []

        # touver l'Index du film dans la matrice
        idx = self.movie_ids.index(movie.id)

        # Calcule la similarité entre ce film et tous les autres
        similarities = cosine_similarity(
            self.tfidf_matrix[idx],
            self.tfidf_matrix
        ).flatten() #Compare le vecteur du film choisi avec tous les autres vecteurs de la matrice

        # Trie par similarité décroissante (ignore le film lui-même)
        similar_indices = np.argsort(similarities)[::-1]

        results = [] # Ajoute les films jusqu'à avoir n résultats.
        for i in similar_indices:            #Parcourt les films du plus similaire au moins similaire
            if self.movie_ids[i] != movie.id:
                results.append((self.db.movies[i], round(similarities[i], 2)))
            if len(results) >= n:
                break

        return results

    def recommend_from_history(self, user, n=5):
        """
        Recommande des films basé sur l'historique de l'utilisateur.
        Trouve les films similaires aux films que l'utilisateur a aimés.
        """
        if not user.ratings:
            return []

        seen = {r.movie.id for r in user.ratings} #films déjà vus

        # Films bien notés par l'utilisateur
        liked_movies = [r.movie for r in user.ratings if r.is_positive()]   #uniquement les films que l'utilisateur a aimés (note ≥ 3)

        if not liked_movies:
            return []

        # Accumule les scores de similarité
        scores = {}
        #Si le film apparaît plusieurs fois (similaire à plusieurs films aimés), additionne les scores 
        for liked_movie in liked_movies:
            similar = self.get_similar_movies(liked_movie, n=10)
            for movie, sim_score in similar:
                if movie.id not in seen:
                    if movie.id not in scores:
                        scores[movie.id] = (movie, sim_score)
                    else:
                        scores[movie.id] = (movie, scores[movie.id][1] + sim_score)

        # Trie et retourne les meilleurs
        sorted_movies = sorted(scores.values(), key=lambda x: x[1], reverse=True)
        return [movie for movie, score in sorted_movies[:n]]