# Kod: Engelska
# Kommentarer: Svenska
# Access layer, FastAPI endpoints för min databas
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import (
    func,
)  # <-- NY: För att kunna slumpa glosor i DB. Få ut 10x första random glosor via /terms endpoint

# Importera min databas och modeller och pydantic schema
from src.database import SessionLocal
from src.models import Term
from src.schemas import TermResponse  # <-- ny ifrån schemas.py

# Själva applikationen
app = FastAPI(
    title="Johnnys Glossary API",
    description="An API to get Data Engineering glossary terms",
    version="1.0.0",
)


# Dependency Injection: En funktion som ger mig en databas session för varje anrop
def get_db():
    db = SessionLocal()
    try:
        yield db  # Här "lånas sessionen" / "öppnas dörren"
    finally:
        db.close()  # Här "stängs dörren till sessionen"


# --- Mina Endpoints (Vägar in till "huset") ---
@app.get("/")
def root():
    return {"message": "Welcome to my Glossary API. Use the /docs endpoint"}


# Health check endpoint
@app.get("/health", tags=["System"])
def health_check(db: Session = Depends(get_db)):
    """A simple health check to ensure the API and DB are up, running and well."""

    try:  # Skickar en extremt enkel fråga ("SELECT 1") för att tvinga fram ett anrop till Postgres
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:  # Släng 503 error om DB ej svarar
        raise HTTPException(status_code=503, detail="Database connection failed")


# FÖRSTA endpoint: Säger åt FastAPI att svaret ska vara en lista av TermResponse-objekt
@app.get("/terms", response_model=list[TermResponse])
def get_terms(db: Session = Depends(get_db)):
    """Gets the first 10 RANDOM terms from the Database"""
    # order_by(func.random()) tvingar postgres att shuffla kortleken innan den tar upp 10 nya glosor
    stmt = (select(Term).order_by(func.random()).limit(10))  
    terms = db.scalars(stmt).all()
    # Returnerar bara listan med SQAlchemy object rakt av.
    # Pydantic (via response_model) tittar på objekten, läser model_config = ConfigDict(from_attributes=True)
    # och gör automatiskt om allting till JSON i bakgrunden.
    return terms


# ANDRA endpoint: Hämta SPECIFIK glosa via dens SLUG
@app.get("/terms/{term_slug}", response_model=TermResponse)
def get_term_by_slug(term_slug: str, db: Session = Depends(get_db)):
    """Searches for a SPECIFIC term via its URL slug (ex, /terms/git)"""
    stmt = select(Term).where(Term.slug == term_slug)
    term = db.scalars(stmt).first()

    if not term:
        # Error handling. Felmeddelande om en viss slug ej existerar.
        raise HTTPException(status_code=404, detail=f"Term {term_slug} was not found.")
    return term


# TREDJE endpoint: RANDOM GLOSA.
@app.get("/random", response_model=TermResponse)
def random_term(db: Session = Depends(get_db)):
    """Gets A random term from the database"""
    stmt = select(Term).order_by(func.random()).limit(1)
    term_rnd = db.scalars(stmt).first()
    return term_rnd
