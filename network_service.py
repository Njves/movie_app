import requests
import json


class NetworkService:
    __kinopoisk_api = "https://kinopoiskapiunofficial.tech"
    __api_key = "c7f4df9c-867c-480c-b94a-a171503eeed4"
    __api_paths = {
        "top": "/api/v2.2/films/top"
    }

    def __init__(self):
        pass

    def get_top_films(self, page):
        r = requests.get(
            url=self.__kinopoisk_api + self.__api_paths["top"] + "?type=TOP_250_BEST_FILMS&page={0}".format(page),
            headers={"accept": "application/json", "X-API-KEY": self.__api_key})
        print(r.json())
        if r.status_code == 200:
            return r.json()['films']
        else:
            return []

    def get_film(self, movie_id):
        r = requests.get(
            url=self.__kinopoisk_api + f"/api/v2.1/films/{movie_id}",
            headers={"accept": "application/json", "X-API-KEY": self.__api_key})
        if r.status_code == 200:
            return r.json()
        else:
            return []
