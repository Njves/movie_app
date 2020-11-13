import os
import sqlite3

import requests

from movie_app.movie import Movie
from movie_app.network_service import NetworkService
from movie_app.res_owner import ResourceOwner


class MovieDatabase:
    _table_name = "movie"
    _genre_table_name = "genres"
    def __init__(self):
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
        )""".format(self._table_name))
        self.db.commit()
        self.cursor.close()
        self.create_genre_table()


    def create_genre_table(self):
        self.cursor = self.db.cursor()
        self.cursor.execute(f""" CREATE TABLE IF NOT EXISTS {self._genre_table_name}(id INT, title TEXT)""")
        self.cursor.close()

    def make_movie_list(self, data):
        movie_list = []
        for i in data:
            movie_list.append(Movie(i[1],i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))
        return movie_list

    def get_movie_list(self):
        cursor = self.db.cursor()
        cursor.execute(f"SELECT * FROM {self._table_name}")
        result = cursor.fetchall()
        movie_list = self.make_movie_list(result)

        cursor.close()
        return movie_list

    def add_movie(self, movie):
        if not isinstance(movie, Movie):
            return False

        cursor = self.db.cursor()
        try:
            cursor.execute(f"INSERT INTO {self._table_name} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
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
        cursor.execute(f"DELETE FROM {self._table_name} WHERE title = ?", (movie.title,))
        #self.db.commit()
        cursor.close()
        return True

    def clear_table(self):
        cursor = self.db.cursor()
        cursor.execute(f"DELETE FROM {self._table_name}")
        self.db.commit()
        cursor.close()
        return True

    def change_image_path(self):
        m_list = ResourceOwner().get_images()
        cursor = self.db.cursor()
        for i in m_list:
            query = f"UPDATE {self._table_name} SET image_path = '{i}' WHERE "
            cursor.execute(query)

    def search_by_title(self, query):
        cursor = self.db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self._table_name} WHERE title LIKE '{query}%'")
        except sqlite3.DatabaseError as e:
            print(e)
        data = cursor.fetchall()
        movie_list = self.make_movie_list(data)
        cursor.close()
        return movie_list

    def search_by_genre(self, query):
        cursor = self.db.cursor()
        try:
            cursor.execute(f"SELECT * FROM {self._table_name} WHERE genre = {query}")
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
            cursor.execute(f"SELECT * FROM {self._table_name} ORDER BY rating {query}")
        except sqlite3.DatabaseError as e:
            print(e)
        data = cursor.fetchall()
        movie_list = self.make_movie_list(data)
        cursor.close()
        return movie_list



