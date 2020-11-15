import os
import sqlite3
import uuid

import requests

from movie import Movie
from network_service import NetworkService
from res_owner import ResourceOwner
import logging

logging.basicConfig(filename="app.log", filemode="w")


class MovieDatabase:
    __movie_table_name = "movie"
    __genre_table_name = "genres"
    __type_table_name = "type"
    __favorite_table_name = None
    def __init__(self):

        logging.info("db movie init")
        self.db = sqlite3.connect("movie.db")
        self.cursor = self.db.cursor()
        self.cursor.execute(""" CREATE TABLE IF NOT EXISTS {0}(
            uid TEXT,
            title TEXT,
            title_ru TEXT,
            created_date INT,
            image_path TEXT,
            country TEXT,
            rating REAL,
            description TEXT,
            genre INT,
            movie_type TEXT
        )""".format(self.__movie_table_name))
        self.db.commit()
        self.cursor.close()
        self.create_genre_table()
        self.create_type_table()

    def create_genre_table(self):
        cursor = self.db.cursor()
        cursor.execute(f""" CREATE TABLE IF NOT EXISTS {self.__genre_table_name}(title TEXT)""")
        cursor.execute(f""" SELECT * FROM {self.__genre_table_name}""")
        genres = cursor.fetchall()
        print(len(genres))
        if len(genres) <= 0:
            self.cursor.executemany(f""" INSERT INTO {self.__genre_table_name} VALUES(?,?)""", [(0, "боевик"),
                                                                                                (1, "драма"),
                                                                                                (2, "комедия"),
                                                                                                (3, "фантастика"),
                                                                                                (4, "триллер")])
            self.db.commit()
        cursor.close()

    def create_type_table(self):
        cursor = self.db.cursor()
        cursor.execute(f""" CREATE TABLE IF NOT EXISTS {self.__type_table_name}(id, title TEXT) """)
        cursor.execute(f""" SELECT * FROM {self.__type_table_name} """)
        types = cursor.fetchall()
        if len(types) <= 0:
            cursor.executemany(f""" INSERT INTO {self.__type_table_name} VALUES(?, ?)""", [(0, "фильм"), (1, "сериал")])
            self.db.commit()
        cursor.close()

    def create_favorite_table(self):
        cursor = self.db.cursor()
        cursor.execute(f""" CREATE TABLE IF NOT EXISTS {self.__favorite_table_name} ()""")
        self.db.commit()
        cursor.close()

    def get_movie_type(self):
        cursor = self.db.cursor()
        cursor.execute(f""" SELECT * FROM {self.__type_table_name}""")
        types = cursor.fetchall()
        print(types)
        cursor.close()
        return types

    def make_movie_list(self, data):
        movie_list = []
        for i in data:
            movie_list.append(Movie(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))
        return movie_list

    def make_movie_from_tuple(self, tuple_movie):
        request = requests.get(tuple_movie['posterUrlPreview'])
        image = ResourceOwner().download_image(request.content)
        return Movie(uuid.uuid4(), tuple_movie['nameEn'], tuple_movie['nameRu'], tuple_movie['year'], image,
                     tuple_movie['countries'][0]['country'], 8.0, "",
                     tuple_movie['genres'][0]['genre'], "film")

    def get_movie_list(self):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {self.__movie_table_name}")
        result = cursor.fetchall()
        movie_list = self.make_movie_list(result)

        cursor.close()
        return movie_list

    def get_genres_list(self):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {self.__genre_table_name}")
        result = cursor.fetchall()
        cursor.close()
        return result

    def add_movie(self, movie):
        if not isinstance(movie, Movie):
            return False

        cursor = self.db.cursor()
        try:
            cursor.execute(f"INSERT INTO {self.__movie_table_name} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                movie.id, movie.title, movie.title_ru, movie.created_date, movie.image_path, movie.country,
                movie.rating,
                movie.description,
                movie.genres,
                movie.movie_type))
        except sqlite3.DatabaseError as e:
            print(e)

        self.db.commit()
        cursor.close()
        return True

    def delete_movie(self, movie):
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM {self.__movie_table_name} WHERE title = ?", (movie.title,))
        self.db.commit()
        cursor.close()
        return True

    def clear_table(self):
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM {self.__movie_table_name}")
        self.db.commit()
        cursor.close()
        return True

    def update_movie(self, movie):
        cursor = self.db.cursor()
        print(f"""UPDATE {self.__movie_table_name} SET title_ru = '{movie.title}',
                        created_date = {movie.created_date},
                        image_path = {movie.image_path},
                        country = {movie.country},
                        rating = {movie.rating},
                        genre = {movie.genres},
                        movie_type = {movie.movie_type}
                        WHERE title = {movie.title}
                        """)
        cursor.execute(f""" UPDATE {self.__movie_table_name} SET title_ru = '{movie.title_ru}',
                        created_date = '{movie.created_date}',
                        image_path = '{movie.image_path}',
                        country = '{movie.country}',
                        rating = '{movie.rating}',
                        genre = '{movie.genres}',
                        movie_type = '{movie.movie_type}'
                        WHERE uid = '{movie.uid}'
                        """)
        self.db.commit()
        cursor.close()

    def change_image_path(self):
        m_list = ResourceOwner().get_images()
        cursor = self.db.cursor()
        for i in m_list:
            query = f"UPDATE {self.__movie_table_name} SET image_path = '{i}' WHERE "
            cursor.execute(query)

    def search_by_title(self, query):
        cursor = self.db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.__movie_table_name} WHERE title_ru LIKE '{query}%'")
        except sqlite3.DatabaseError as e:
            print(e)
        data = cursor.fetchall()
        movie_list = self.make_movie_list(data)
        cursor.close()
        return movie_list

    def search_by_genre(self, query):
        cursor = self.db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self.__movie_table_name} WHERE genre = {query}")
        except sqlite3.DatabaseError as e:
            print(e)
        data = cursor.fetchall()
        cursor.close()
        return data

    def search_by_rating(self, by):
        cursor = self.db.cursor()
        query = "DESC"
        if not by:
            query = "ASC"
        try:
            cursor.execute(f"SELECT * FROM {self.__movie_table_name} ORDER BY rating {query}")
        except sqlite3.DatabaseError as e:
            print(e)
        data = cursor.fetchall()
        movie_list = self.make_movie_list(data)
        cursor.close()
        return movie_list

    def search_by_year(self):
        cursor = self.db.cursor()
        query = f"SELECT * FROM {self.__movie_table_name} ORDER BY created_date DESC"
        try:
            cursor.execute(query)
        except sqlite3.DatabaseError as e:
            print(e)
        sort_list = cursor.fetchall()
        sorted_movie_list = self.make_movie_list(sort_list)
        return sorted_movie_list

    def parse_movie_from_json(self):
        service = NetworkService()
        page = 2
        # top = service.get_top_films(page)
        # for i in top:
        #    movie = self.make_movie_from_tuple(i)
        #    self.add_movie(movie)
        #    print(f"Загрузка {i}")

    def parse_movie(self):
        film = NetworkService().get_film()['data']
        if len(film) > 0:
            movie = self.make_movie_from_tuple(film)
            self.add_movie(movie)
            print(f"Загрузка {film}")
