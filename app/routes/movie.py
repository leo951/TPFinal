from bson import ObjectId
# from debugpy import connect
from fastapi import APIRouter, HTTPException, status

from app.models.movie import Movie
from app.config.db import dbMovie
from app.schemas.movie import movieEntity, moviesEntity

movie = APIRouter()

@movie.get('/', response_description="Get all movies")
async def find_all_movies():
    return moviesEntity(dbMovie.find())

@movie.get('/{id}', response_model=Movie, response_description="Get a Movie")
async def find_one_movie(id): 
    return movieEntity(dbMovie.find_one({"_id": ObjectId(id)}))

@movie.post('/', response_model=Movie, response_description="Add a movie", status_code=status.HTTP_201_CREATED)
async def create_movie(movie: Movie):
    dbMovie.insert_one(dict(movie))
    x = dbMovie.find()
    print(x)
    return movieEntity(x[0])

@movie.put('/{id}', response_description="Update a movie", status_code=status.HTTP_204_NO_CONTENT)
async def update_movie(id, movie: Movie):
    dbMovie.find_one_and_update({"_id": ObjectId(id)}, {
        "$set":dict(movie)
    })
    return movieEntity(dbMovie.find_one({"_id": ObjectId(id)}))

@movie.delete('/{id}', response_description="Delete a movie", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(id, movie: Movie):
    return movieEntity(dbMovie.find_one_and_delete({"_id": ObjectId(id)}))
