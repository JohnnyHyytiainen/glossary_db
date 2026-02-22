# Kod: Engelska
# Kommentarer: Svenska
# Access layer, FastAPI endpoints för min databas
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
# Importera min databas och modeller och pydantic schema
from src.database import SessionLocal
from src.models import Term
from src.schemas import TermResponse # <-- ny ifrån schemas.py

# Själva applikationen
app = FastAPI(
    title="Johnnys Glossary API",
    description="An API to get Data Engineering glossary terms",
    version="1.0.0"
)

# Dependency Injection: En funktion som ger mig en databas session för varje anrop
def get_db():
    db = SessionLocal()
    try:
        yield db # Här "lånas sessionen" / "öppnas dörren"
    finally:
        db.close() # Här "stängs dörren till sessionen"

# --- Mina Endpoints (Vägar in till "huset") ---

@app.get("/")
def root():
    return {"message": "Welcome to my Glossary API. Use the /docs endpoint"}

# NYTT: Säger åt FastAPI att svaret ska vara en lista av TermResponse-objekt
@app.get("/terms", response_model=list[TermResponse])
def get_all_terms(db: Session = Depends(get_db)):
    """Gets the first 10 terms from the Database"""
    stmt = select(Term).limit(10)
    terms = db.scalars(stmt).all()

    # Returnerar bara listan med SQAlchemy object rakt av.
    # Pydantic (via response_model) tittar på objekten, läser model_config = ConfigDict(from_attributes=True)
    # och gör automatiskt om allting till JSON i bakgrunden.
    return terms
