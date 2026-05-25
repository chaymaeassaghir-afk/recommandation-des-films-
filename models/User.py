from models.Person import Person
from models.Rating import Rating

class User(Person):
    def __init__(self, name, email,id=None):
        super().__init__( name)
        self.__id = id
        self.__email = email
        self.__ratings = []

    @property
    def id(self):
        return self.__id

    @property
    def email(self):
        return self.__email

    @property
    def ratings(self):
        return self.__ratings

    def get_info(self):
        return f"Nom : {self.name} | Email : {self.__email}"

    def rate_movie(self, movie, score):
        rating = Rating(self, movie, score)
        self.__ratings.append(rating)
        return rating

    def get_recs(self):
        pass  