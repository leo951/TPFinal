from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    director: str
    actor: str
    duration: int