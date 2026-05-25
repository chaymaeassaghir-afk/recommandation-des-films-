from engine.RecommendationEngine import RecommendationEngine
from engine.tfidf import TFIDFEngine

class movieController:
    def __init__(self,db,engine,tfidf):
        self.db=db
        self.engine=engine
        self.tfidf=tfidf

    def get_catalogue(self):
        return self.db.movies

    def noter_film(self,user,movie_id,score):
        movie = self.db.find_movie(movie_id) 
        if not movie :
            return None
        c=0 
        for r in user.ratings :
            if r.movie.id==movie_id :
                c=1
        if c==1:
            return "deja noter"
        user.rate_movie(movie,score)
        self.db.save_rating(user,movie,score)
        return movie

    

    def get_recommandations(self, user, n=10):
        return self.engine.recommend_hybrid(user, n)  

    def get_recommandations_genre(self, user, genre, n=5):
        return self.engine.filter_by_genre(user, genre, n)

    def get_historique(self,user):
        return user.ratings

                

