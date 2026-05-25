class Movie:
    def __init__(self, id, title, genre, year ,image="",description=""):
        self.__id = id
        self.__title = title
        self.__genre = genre
        self.__year = year
        self.__avg_score = 0
        self.__image = image
        self.__description = description

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def genre(self):
        return self.__genre

    @property
    def year(self):
        return self.__year

    @property
    def avg_score(self):
        return self.__avg_score

    @property
    def description(self):
        return self.__description   

    @property
    def image(self):
        return self.__image     

    @avg_score.setter
    def avg_score(self, value):
        self.__avg_score = value

    def get_details(self):
        return f"[{self.__id}] {self.__title} | {self.__genre} | {self.__year} | Note moyenne : {self.__avg_score}/5"