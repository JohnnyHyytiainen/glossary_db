# Kod: Engelska
# Kommentarer: Svenska
# Schemas med pydantic. Definierar kontraktet för hur mina glosor(Terms) ska se ut för användaren
from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.models import DifficultyLevel

# --- 1: Sub-schemas (relationer) ---

class CategoryResponse(BaseModel): # Schema för att få fram Category
    id: int
    name: str

    # Min "bro" för Pydantic till SQLAlchemy. Säger åt Pydantic att läsa direkt ifrån SQLAlchemy object
    model_config = ConfigDict(from_attributes=True)

# TODO: FYLL I SOURCES MED LÄNKAR FÖR VARJE GLOSA!!!
class SourceResponse(BaseModel):
    id: int
    name: str
    url: Optional[str] = None # Bra att ha med URL om jag fyller i mina sources med links 

    # Min "bro" för Pydantic till SQLAlchemy. Säger åt Pydantic att läsa direkt ifrån SQLAlchemy object
    model_config = ConfigDict(from_attributes=True)


# --- 2: Main Schema ---

# "Svars kontraktet", det mitt API skickar TILL användaren(Vad user ser)
class TermResponse(BaseModel):
    id: int
    slug: str
    term: str
    definition: str # <-- NY: För att få ut definitionen av glosan.
    difficulty: Optional[DifficultyLevel] = None

    # THE NESTED MAGIC: Här säger jag att varje Term har en lista av Kategorier och Källor
    categories: list[CategoryResponse] = []
    sources: list[SourceResponse] = []

    # Min "bro" för Pydantic till SQLAlchemy. Säger åt Pydantic att läsa direkt ifrån SQLAlchemy object
    model_config = ConfigDict(from_attributes=True)

# --- 3: Input för min ASK endpoint ---
# Det användare ska SKICKA till mitt API
class AskRequest(BaseModel):
    query: str

# --- 3: OUTPUT för min ASK endpoint ---
# Det användare får SVAR på från mitt API
class AskResponse(BaseModel):
    query: str
    answer: str
