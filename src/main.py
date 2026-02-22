# Kod: Engelska
# Kommentarer: Svenska
# Access layer, FastAPI endpoints för min databas
from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
# Importera min databas och modeller
from src.database import SessionLocal
from src.models import Term

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

@app.get("/terms")
def get_all_terms(db: Session = Depends(get_db)):
    """Gets the first 10 terms from the Database"""
    # Gör en enkel SELECT * FROM terms LIMIT 10;
    stmt = select(Term).limit(10)
    terms = db.scalars(stmt).all()

    # Formaterar svaret fint till en lista med lexikon(?) (JSON)
    result = []
    for t in terms:
        result.append({
            "id": t.id,
            "term": t.term,
            "slug": t.slug,
            "difficulty": t.difficulty.value if t.difficulty else None
        })
    return {"data": result}