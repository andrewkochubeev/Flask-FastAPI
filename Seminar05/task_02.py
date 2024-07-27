import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

movies = []


class Genre(Enum):
    genre_1 = 'boevik'
    genre_2 = 'fantastika'
    genre_3 = 'comedy'


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: Genre


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/movies/{genre}")
async def get_movies_for_genre(genre: Genre):
    out = []
    for movie in movies:
        if movie.genre == genre:
            out.append(movie)
    return out


@app.post("/movies/")
async def create_movie(movie: Movie):
    movies.append(movie)
    return movies


if __name__ == '__main__':
    uvicorn.run('task_02:app', reload=True)
