# Kod: Engelska
# Kommentarer: Svenska
# Schemas med pydantic. Definierar kontraktet för hur mina glosor(Terms) ska se ut för användaren
from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.models import DifficultyLevel

# "Svars kontraktet", det mitt API skickar TILL användaren(Vad user ser)
class TermResponse(BaseModel):
    id: int
    slug: str
    term: str
    difficulty: Optional[DifficultyLevel] = None

    # Min "bro" för Pydantic till SQLAlchemy. Säger åt Pydantic att läsa direkt ifrån SQLAlchemy object
    model_config = ConfigDict(from_attributes=True)