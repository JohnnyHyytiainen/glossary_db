# Kod: Engelska
# Kommentarer: Svenska
# För att läsa/ladda in alla 195x glosor från ren och ifylld csv -> postgres glossary db
import re
import pandas as pd
from sqlalchemy import select
from src.database import SessionLocal
from src.models import Term, Category, Source, DifficultyLevel

def generate_slug(text: str, _) -> str:
    """
    Helper function to clean name and create a URL friendly slug.
    Example: 'Primary Key (PK)' -> 'primary-key-pk'
    """
    text = str(text).lower().strip()
    # Var noga med att ha med viktiga tecken som kan behövas, t.ex 'cd ...'
    text = text.replace('..', 'dotdot')
    text = text.replace('c++', 'cpp')
    # Byt ut allt som inte är bokstäver/siffror mot bindestreck
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def load_data_from_csv():
    csv_file = "data/glossary_filled_clean.csv"

    print(f"Loading: Reading {csv_file}...")

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Could not find file {csv_file}. Check pathing")
        return
    
    db = SessionLocal()
    # NYTT: En mängd (set) för att hålla koll på vilka slugs jag processat i denna körning
    seen_slugs = set()

    try:
        # loopa igenom varje rad i CSV
        for index, row in df.iterrows():
            term_name = str(row['Term']).strip()
            definition = str(row['Definition']).strip()
            category_name = str(row['Category']).strip()
            source_name = str(row['Source']).strip()

            # skapa slug
            slug = generate_slug(term_name, seen_slugs)

            # 1: Hämta eller skapa Category
            category = db.scalars(select(Category).where(Category.name == category_name)).first()
            if not category:
                category = Category(name=category_name,description=f"Terms in: {category_name}")
                db.add(category)
                db.flush() # db.flush() skickar till databasen för att få ett ID men committar ingenting än

            # 2: Hämta eller skapa källa
            source = db.scalars(select(Source).where(Source.name == source_name)).first()
            if not source:
                source = Source(name=source_name, source_type="Course")
                db.add(source)
                db.flush()

            # 3: Hämta eller skapa Term. Det är här klassen kommer in. Se seed.py
            term = db.scalars(select(Term).where(Term.slug == slug)).first()
            if not term:
                term = Term(
                    slug=slug,
                    term=term_name,
                    definition=definition,
                    difficulty=DifficultyLevel.beginner, # Default. Får se över om jag kan göra ändringar manuellt när allt är stabilt
                    categories=[category],
                    sources=[source]
                )
                db.add(term)
            else:
                # OM term redan finns, se till att mina junction tables är uppdaterade
                if category not in term.categories:
                    term.categories.append(category)
                if source not in term.sources:
                    term.sources.append(source)

        # 4: Spara allting(db commit)
        db.commit()
        print(f"Loading {len(df)} rows to PostgreSQL DB....")

    except Exception as e:
        print(f"Error occured when ingesting {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    load_data_from_csv()