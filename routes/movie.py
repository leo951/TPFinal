from http.client import HTTPException
from telnetlib import STATUS
from bson import ObjectId
from debugpy import connect
from fastapi import APIRouter, HTTPException, status, body

from models.movie import Movie
from config.db import dbMovie
from schemas.movie import movieEntity, moviesEntity
movie = APIRouter()

@movie.get('/')
async def find_all_movies():
    return moviesEntity(dbMovie.find())

@movie.get('/{id}')
async def find_one_movie(id): 
    return movieEntity(dbMovie.find_one({"_id": ObjectId(id)}))

@movie.post('/')
async def create_movie(movie: Movie):
    dbMovie.insert_one(dict(movie))
    x = dbMovie.find()
    return moviesEntity(x[0])

@movie.put('/{id}')
async def update_movie(id, movie: Movie):
    dbMovie.find_one_and_update({"_id": ObjectId(id)}, {
        "$set":dict(movie)
    })
    return movieEntity(dbMovie.find_one({"_id": ObjectId(id)}))

@movie.delete('/{id}')
async def delete_movie(id, movie: Movie):
    return movieEntity(dbMovie.find_one_and_delete({"_id": ObjectId(id)}))
