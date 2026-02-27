# Kod: Engelska
# Kommentarer: Svenska
# För att läsa/ladda in alla 195x glosor från ren och ifylld csv -> postgres glossary db
import re
import pandas as pd
from sqlalchemy import select
from src.database import SessionLocal
from src.models import Term, Category, Source, DifficultyLevel

# Skapa 'translation map' för kända specialfall/edge cases
# Här får jag mappa vad extremfallen ska heta i URL'en
CUSTOM_SLUGS = {
        "*args":"args",
        "**kwargs": "kwargs",
        "__repr__": "dunder-repr",
        "__init__": "dunder-init",
        "__str__": "dunder-str",
        "__iter__": "dunder-iter",
        "c++": "cpp",
        "cd ..": "cd-dotdot",
        "c#": "c-sharp",
        "docker exec -it": "docker-exec-it"
    }

def generate_slug(text: str) -> str:
    """
    Helper function to clean name and create a URL friendly slug.
    Example: 'Primary Key (PK)' -> 'primary-key-pk'.
    Respecting Python/Docker syntax.
    """

    # 1) Rensa markdown escapes direkt. (t.ex \*args blir *args)
    clean_text = str(text).replace("\\", "").strip().lower()


    # 2) Om termen finns i min mapping för CUSTOM SLUGS, returnera översättningen direkt
    if clean_text in CUSTOM_SLUGS:
        return CUSTOM_SLUGS[clean_text]
    
    # 4) Om det inte är ett specialfall/edge case kör standard slug generating
    # Byt ut allt som inte är bokstäver/siffror mot bindestreck - 
    slug = re.sub(r'[^a-z0-9]+', '-', clean_text)

    # Rensa upp multibla bindestreck, --- blir - och bindestreck i ändarna
    slug = re.sub(r'-+', '-', slug).strip('-')
    
    return slug

def load_data_from_csv():
    csv_file = "data/glossary_filled_unique_terms.csv"

    print(f"Loading: Reading {csv_file}...")

    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Could not find file {csv_file}. Check pathing")
        return
    
    db = SessionLocal()

    try:
        # loopa igenom varje rad i CSV
        for index, row in df.iterrows():
            # Tvätta bort markdown escapes direkt
            term_name = str(row['Term']).replace("\\", "").strip()
            definition = str(row['Definition']).strip()
            category_name = str(row['Category']).strip()
            source_name = str(row['Source']).strip()

            # skapa slug
            slug = generate_slug(term_name)

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