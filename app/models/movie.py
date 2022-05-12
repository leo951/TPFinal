from dataclasses import Field
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field()
    director: str = Field()
    actor: str = Field()
    duration: int = Field()