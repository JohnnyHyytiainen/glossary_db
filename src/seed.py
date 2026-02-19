# Kod: Engelska
# Kommentarer: Svenska
# För att seeda(fylla på min databas v1)
from src.database import SessionLocal, engine, Base
from src.models import Term, Category, Source, DifficultyLevel
from sqlalchemy import select

# 1. Öppna min session
def seed_data():
    db = SessionLocal()

    try:
        print("Seeding database...")


        # --- Phase 1: TRANSIENT (Skapa python object i minnet(RAM, temp storage)) ---
        # Steg 1: Skapa mina kategorier(categories table i min postgres db)
        cat_devops = Category(name="DevOps", description="Development + Operations")
        cat_coding = Category(name="Coding", description="Writing code, programming")

        # Steg 2: Skapa mina Sources(sources table i min postgres db)
        src_course = Source(name="Data Engineer 2025", source_type="Course")
        src_docs = Source(name="Python Docs", source_type="Documentation", url="https://docs.python.org")

        # Steg 3: Skapa Termer och koppla dom direkt i minnet
        # NOTE: Du kopplar ihop dom med Kategorier direkt!
        term_cicd = Term(
            slug="ci-cd",
            term="CI/CD",
            definition="Continuous Integration / Continuous Deployment. Automating the pipeline.",
            difficulty=DifficultyLevel.intermediate,
            categories=[cat_devops], # SQLAlchemy fattar att den ska använda min junction table automatiskt
            sources=[src_course]
        )

        term_python = Term(
            slug="python",
            term="Python",
            definition="A high level programming language used for AI development and a general purpose language",
            difficulty=DifficultyLevel.beginner,
            categories=[cat_coding, cat_devops], # Två kategorier!
            sources=[src_docs] 
        )

        # --- Phase 2: PENDING (Lägg i väntrummet) ---
        # Du behöver bara lägga till termerna. SQLAlchemy är smart nog att se att
        # kategorierna och källorna sitter fast i termerna, så de följer med automatiskt!
        # Steg 4: Lägg till i nuvarande session.
        db.add(term_cicd)
        db.add(term_python)

        # --- Phase 3: PERSISTENT (HÄR skickas det till DB för permanent storage) ---
        # Steg 5: Spara(tänk commit i git)
        db.commit()
        print("Data seeded successfully. Check your PgAdmin4!")

        # Steg 6: Verifiera, läs tillbaka(säkertställer paritet)
        # efter db.commit() skickar SQAlchemy ett SELECT statement till postgres via db.scalars(stmt).one()
        # db.scalars(stmt).one() gör alltså en SELECT av sig själv!
        stmt = select(Term).where(Term.slug == "python")
        result = db.scalars(stmt).one()
        print(f"\n - Verifierar: Hittade termen '{result.term}'")
        print(f"   - Kategorier: {[c.name for c in result.categories]}")
        print(f"   - Sources: {[s.name for s in result.sources]}")




    except Exception as e:
        print(f"Error with seeding the data: {e}")
        db.rollback() # <---- Rollback, rullar tillbaka allting om något går fel (Om jag försöker lägga in dubbletter t.ex)
    finally:
        db.close() # <---- VIKTIGT. ALLTID STÄNGA "DÖRREN"

if __name__ == "__main__":
    seed_data()