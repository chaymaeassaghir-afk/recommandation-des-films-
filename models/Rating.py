class Rating:
    def __init__(self, user, movie, score):
        if score < 1 or score > 5:
            raise ValueError("La note doit être entre 1 et 5")
        self.__user = user
        self.__movie = movie
        self.__score = score

    @property
    def user(self):
        return self.__user

    @property
    def movie(self):
        return self.__movie

    @property
    def score(self):
        return self.__score

    def is_positive(self):
        return self.__score >= 3