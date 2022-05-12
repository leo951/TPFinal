from fastapi import FastAPI
from app.routes.movie import movie
app = FastAPI()

app.include_router(movie)