import uuid


class Movie:
    # TODO: Добавить длительность
    def __init__(self, title, title_ru, created_date, image_path, country, rating, description, genres, movie_type):
        self._id = uuid.uuid1()
        self.title = title
        self.title_ru = title_ru
        self.created_date = created_date
        self.image_path = image_path
        self.country = country
        self.rating = rating
        self.description = description
        self.genres = genres
        self.duration = 120
        self.movie_type = movie_type



    @property
    def id(self) -> str:
        return str(self._id)

    def __str__(self) -> str:
        return f"id: {self.id}, title: {self.title}, date: {self.created_date}, image_path: {self.image_path}," \
               f"country: {self.country}, description: {self.description}, genres: {self.genres}, movie_type: {self.movie_type}"



