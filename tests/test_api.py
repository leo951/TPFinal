from bson import ObjectId
import requests
from unittest import TestCase
from fastapi import status
from app.config.db import dbMovie

from app.models.movie import Movie

class TestApi(TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8000'
        self.data = {
            "title": "star wars",
            "director": "George Lucas",
            "actor": "Harrison Ford",
            "duration": 121
        }
        self.dataUpdated = {
            "name": "star wars IV",
            "director": "George Lucas",
            "actor": "Harrison Ford",
            "duration": 121
        }

        self.reqCreated = requests.post(self.url, json=self.data)
        self.newMovie = Movie(**self.reqCreated.json())

        self.reqGetAll = requests.get(f'{self.url}/')
        self.movies = [Movie(**movie) for movie in self.reqGetAll.json()]

        getMovie = dbMovie.find_one(self.reqCreated.json())
        self.idMovie = getMovie["_id"]

        self.reqGetbyId = requests.get(f'{self.url}/{self.idMovie}')
        self.movie = Movie(**self.reqGetbyId.json())

        self.dataUpdated['_id'] = str(self.idMovie)
        self.reqUpdated = requests.put(f'{self.url}/{self.idMovie}', json=self.dataUpdated)
        self.reqGetAfterUpdate = requests.get(f'{self.url}/{self.idMovie}')

        self.movieAfterUpdate = Movie(**self.reqGetAfterUpdate.json())

        self.reqDeleted = requests.delete(f'{self.url}/{self.idMovie}')
        print("Je suis request.delete = ",f'{self.url}/{self.idMovie}')
        self.reqGetAfterDelete = requests.get(f'{self.url}/{self.idMovie}')

        #Erreur lors du delete -> renvoie code 422


    def teardown(self):
        pass

    def test_GetAll(self):
        self.assertIsInstance(self.movies, list)
        self.assertIsInstance(self.movies[0], Movie)
        self.assertEqual(self.reqGetAll.status_code, status.HTTP_200_OK)

    def test_GetById(self):
        self.assertIsInstance(self.movie, Movie)
        self.assertIsInstance(self.idMovie, ObjectId)

        self.assertEqual(self.movie.title, self.data['title'])
        self.assertEqual(self.movie.director, self.data['director'])
        self.assertEqual(self.movie.actor, self.data['actor'])
        self.assertEqual(self.movie.duration, self.data['duration'])
        self.assertEqual(self.reqGetbyId.status_code, status.HTTP_200_OK)

    def test_Created(self):
        self.assertIsInstance(self.newMovie, Movie)
        self.assertIsInstance(self.idMovie, ObjectId)

        self.assertEqual(self.newMovie.title, self.data['title'])
        self.assertEqual(self.newMovie.director, self.data['director'])
        self.assertEqual(self.newMovie.actor, self.data['actor'])
        self.assertEqual(self.newMovie.duration, self.data['duration'])
        self.assertEqual(self.reqCreated.status_code, status.HTTP_201_CREATED)

    def test_Updated(self):
        self.assertIsInstance(self.movieAfterUpdate, Movie)
        self.assertIsInstance(self.dataUpdated['_id'], str)

        self.assertEqual(self.movieAfterUpdate.title, self.dataUpdated['title'])
        self.assertEqual(self.movieAfterUpdate.director, self.dataUpdated['director'])
        self.assertEqual(self.movieAfterUpdate.actor, self.dataUpdated['actor'])
        self.assertEqual(self.movieAfterUpdate.duration, self.dataUpdated['duration'])
        self.assertEqual(self.reqUpdated.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleted(self):
        self.assertEqual(self.reqDeleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.reqGetAfterDelete.status_code, status.HTTP_404_NOT_FOUND)