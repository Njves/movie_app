from movie_app.movie import Movie
import os
class MovieManager:

    _movie_list_path = "movies.json"
    def __init__(self):




    def check_exist_movie_file(self):
        return os.path.getsize(self._movie_list_path) > 0
