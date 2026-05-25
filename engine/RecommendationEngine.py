import numpy as np
from sklearn.neighbors import NearestNeighbors

class RecommendationEngine:
    def __init__(self, db, tfidf):
        self.db = db
        self.tfidf_engine = tfidf 
        self.model = NearestNeighbors(metric='cosine', algorithm='brute') 
        self.user_ids = []
        self.movie_ids = []
        #la matrice utilisateurs × films 
        self.matrix = None
        self.train()

    def train(self):
        self.user_ids = [u.id for u in self.db.users]
        self.movie_ids = [m.id for m in self.db.movies]

        # Crée une matrice vide remplie de 0
        self.matrix = np.zeros((len(self.user_ids), len(self.movie_ids)))

        # Remplit la matrice avec les notes
        for i, user in enumerate(self.db.users):
            for rating in user.ratings:
                if rating.movie.id in self.movie_ids:
                    j = self.movie_ids.index(rating.movie.id)
                    self.matrix[i][j] = rating.score

        # Entraîne le modèle KNN
        if len(self.user_ids) > 1:
            self.model.fit(self.matrix)
            print(f" Modèle KNN entraîné : {self.matrix.shape}")
    
    
    def recommend(self, user, n=7):
        """
        Recommande n films à un utilisateur via KNN.
        Trouve les K voisins les plus proches et collecte leurs films.
        """
        if user.id not in self.user_ids:
            return []

        # Matrice à jour
        self.train()

        seen = {r.movie.id for r in user.ratings}
        idx = self.user_ids.index(user.id)
        user_vector = self.matrix[idx].reshape(1, -1)

        # Trouve les K voisins les plus proches
        k = min(len(self.user_ids), 4)  # max 3 voisins + lui-même
        distances, indices = self.model.kneighbors(user_vector, n_neighbors=k)

        # Collecte les films recommandés par les voisins
        scores = {}
        for i, neighbor_idx in enumerate(indices[0]):
            if neighbor_idx == idx:
                continue  # ignore lui-même

            similarite = 1 - distances[0][i]  # distance cosinus → similarité
            neighbor = self.db.users[neighbor_idx]

            for rating in neighbor.ratings:
                if rating.movie.id not in seen and rating.is_positive():
                    movie_id = rating.movie.id
                    if movie_id not in scores:
                        scores[movie_id] = (rating.movie, similarite * rating.score)
                    else:
                        scores[movie_id] = (rating.movie, scores[movie_id][1] + similarite * rating.score)

        # Trie et retourne les n meilleurs
        sorted_recs = sorted(scores.values(), key=lambda x: x[1], reverse=True)
        return [movie for movie, score in sorted_recs[:n]]        


    

    def compute_similarity(self, u1, u2):
        """
        Calcule la similarité entre deux utilisateurs.
        Utilisé pour affichage ou debug.
        """
        self.train()

        if u1.id not in self.user_ids or u2.id not in self.user_ids:
            return 0

        idx1 = self.user_ids.index(u1.id)
        idx2 = self.user_ids.index(u2.id)

        v1 = self.matrix[idx1].reshape(1, -1)
        v2 = self.matrix[idx2].reshape(1, -1)

        from sklearn.metrics.pairwise import cosine_similarity
        score = cosine_similarity(v1, v2)[0][0]
        return round(score, 2)

    def recommend_hybrid(self, user, n=15):
    
        seen = {r.movie.id for r in user.ratings}

        # ── Scores KNN ──────────────────────────────
        knn_scores = {}
        if len(self.user_ids) > 1:
            self.train()
            idx = self.user_ids.index(user.id) if user.id in self.user_ids else -1

            if idx != -1:
                user_vector = self.matrix[idx].reshape(1, -1)
                k = min(len(self.user_ids), 4)
                distances, indices = self.model.kneighbors(user_vector, n_neighbors=k)

                for i, neighbor_idx in enumerate(indices[0]):
                    if neighbor_idx == idx:
                        continue
                    similarite = 1 - distances[0][i]
                    neighbor = self.db.users[neighbor_idx]
                    for r in neighbor.ratings:
                        if r.movie.id not in seen and r.is_positive():
                            if r.movie.id not in knn_scores:
                                knn_scores[r.movie.id] = (r.movie, 0)
                            knn_scores[r.movie.id] = (
                                r.movie,
                                knn_scores[r.movie.id][1] + similarite * r.score
                            )

        # ── Scores TF-IDF ────────────────────────────
        tfidf_scores = {}
        liked_movies = [r.movie for r in user.ratings if r.is_positive()]

        for liked_movie in liked_movies:
            if liked_movie.id not in self.tfidf_engine.movie_ids:
                continue
            similar = self.tfidf_engine.get_similar_movies(liked_movie, n=10)
            for movie, sim_score in similar:
                if movie.id not in seen:
                    if movie.id not in tfidf_scores:
                        tfidf_scores[movie.id] = (movie, 0)
                    tfidf_scores[movie.id] = (
                        movie,
                        tfidf_scores[movie.id][1] + sim_score
                    )

        # ── Normalisation ────────────────────────────
        # KNN max score
        max_knn = max((s for _, s in knn_scores.values()), default=1)
        # TF-IDF max score
        max_tfidf = max((s for _, s in tfidf_scores.values()), default=1)

        # ── Combinaison ──────────────────────────────
        all_movies = set(knn_scores.keys()) | set(tfidf_scores.keys())
        combined = {}

        for movie_id in all_movies:
            knn_score   = knn_scores[movie_id][1]   / max_knn   if movie_id in knn_scores   else 0
            tfidf_score = tfidf_scores[movie_id][1] / max_tfidf if movie_id in tfidf_scores else 0

            # Poids : 50% KNN + 50% TF-IDF
            final_score = (knn_score * 0.5) + (tfidf_score * 0.5)

            movie = knn_scores[movie_id][0] if movie_id in knn_scores else tfidf_scores[movie_id][0]
            combined[movie_id] = (movie, round(final_score, 3))

        # ── Tri et retour ────────────────────────────
        sorted_recs = sorted(combined.values(), key=lambda x: x[1], reverse=True)
        return [movie for movie, score in sorted_recs[:n]]


    def filter_by_genre(self, user, genre, n=5):
        """
        Filtre les recommandations hybrides par genre.
        """
        all_recs = self.recommend_hybrid(user, n=50)  # large pour avoir assez
        filtered = [m for m in all_recs if m.genre.lower() == genre.lower()]
        return filtered[:n]
                