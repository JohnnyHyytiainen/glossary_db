# Kod: Engelska
# Kommentarer: Svenska
# Access layer, FastAPI endpoints för min databas
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select, text
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.sql.expression import (
    func,
)
from typing import Optional

# Importera min databas och modeller och pydantic schema
from src.database import get_db
from src.models import Term, Category
from src.schemas import TermResponse, AskRequest, AskResponse 
from src.rag import generate_rag_response # <-- ny ifrån rag.py

# Själva applikationen
app = FastAPI(
    title="Johnnys Glossary API",
    description="An API to get Data Engineering glossary terms",
    version="1.0.0",
)


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
# Uppdaterad med Pagination(sidindelning)
@app.get("/terms", response_model=list[TermResponse], tags=["Terms"])
def get_terms(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    category: Optional[str] = None,  # <-- Frivillig filter parameter
    search: Optional[
        str
    ] = None,  # <-- Frivilliga sök parametrar för själva termen(glosan)
    db: Session = Depends(get_db),
):
    """Gets a list of terms Alphabetically with pagination(limit and skip) and optional term or category filtering"""
    # 1) Bygga SQL-fråga (Basen)
    stmt = (
        select(Term)
        .options(selectinload(Term.categories), selectinload(Term.sources))
        .order_by(Term.term)
    )
    # 2) Filter nr ett: Om användaren skickar in en kategori, lägg på ett filter.
    if category:
        # .any() kollar om NÅGON av glosans kategorier matchar sökordet.
        # .ilike() gör sökningen "case-insensitive" (bryr sig inte om stora/små bokstäver)
        stmt = stmt.where(Term.categories.any(Category.name.ilike(f"%{category}%")))

    # 3) Filter nr två: Om användare vill söka i fritext på glosans namn.
    if search:
        stmt = stmt.where(Term.term.ilike(f"%{search}%"))

    # 4) PAGINATION: Lägg på skip och limit sist av allting
    stmt = stmt.offset(skip).limit(limit)
    # 5) EXEKVERING: Skicka förfrågan till Postgres DB
    terms = db.scalars(stmt).all()
    return terms


# ANDRA endpoint: Hämta SPECIFIK glosa via dens SLUG
@app.get("/terms/{term_slug}", response_model=TermResponse)
def get_term_by_slug(term_slug: str, db: Session = Depends(get_db)):
    """Searches for a SPECIFIC term via its URL slug (ex, /terms/git)"""
    stmt = (
        select(Term)
        .options(
            selectinload(Term.categories),
            selectinload(Term.sources),
        )
        .where(Term.slug == term_slug)
    )
    term = db.scalars(stmt).first()

    if not term:
        # Error handling. Felmeddelande om en viss slug ej existerar.
        raise HTTPException(status_code=404, detail=f"Term {term_slug} was not found.")
    return term


# TREDJE endpoint: RANDOM GLOSA.
@app.get("/random", response_model=TermResponse)
def random_term(db: Session = Depends(get_db)):
    """Gets A random term from the database"""
    stmt = (
        select(Term)
        .options(
            selectinload(Term.categories),
            selectinload(Term.sources),
        )
        .order_by(func.random())
        .limit(1)
    )
    term_rnd = db.scalars(stmt).first()

    if not term_rnd:
        raise HTTPException(status_code=404, detail="No terms in database")
    return term_rnd


# Fjärde endpoint: /ask för att lägga till och applicera mitt RAG lager med Gemini API key:
@app.post("/ask", response_model=AskResponse)
def ask_assistant(request: AskRequest):
    """Ask a question to the RAG Data engineer assistant."""
    try:
        # 1) Hämta frågan ifrån pydantic modellen(Schemas.py)
        user_question = request.query
        # 2) Skicka frågan till min RAG engine.
        ai_answer = generate_rag_response(user_question)
        # 3) Returnera datan i de format i min AskResponse schema
        return AskResponse(
            query=user_question,
            answer=ai_answer
        )
    
    except Exception as e: # Fånga och flagga för fel
        raise HTTPException(status_code=500, detail=f"AI stumbled upon an issue: {str(e)}")



