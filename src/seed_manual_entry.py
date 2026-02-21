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
        cat_git = Category(name="Git", description="Git, version control")
        cat_github = Category(name="Github", description="Git but stored on Github")
        cat_gitignore = Category(name="Gitignore", description="gitignore")
        cat_commit = Category(name="Commit", description="Git commit")

        # Steg 2: Skapa mina Sources(sources table i min postgres db)
        src_course = Source(name="Data Engineer 2025", source_type="Course")
        src_docs = Source(name="Python Docs", source_type="Documentation", url="https://docs.python.org")
        src_git = Source(name="Git", source_type="Documentation", url="https://git-scm.com/docs")
        src_github = Source(name="Github", source_type="Documentation", url="https://docs.github.com/en")
        src_gitignore = Source(name="Gitignore", source_type="Documentation", url="https://git-scm.com/docs/gitignore")
        src_commit = Source(name="Commit", source_type="Documentation", url="https://git-scm.com/docs/git-commit")

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

        term_git = Term(
            slug="git",
            term="Git",
            definition="version control system, saves snapshots of every committed change to your code",
            difficulty=DifficultyLevel.intermediate,
            categories=[cat_coding, cat_devops, cat_git, cat_github],
            sources=[src_git]
        )

        term_github = Term(
            slug="github",
            term="Github",
            definition="version control via git BUT cloud-based service you push your changes to. Used to have an extra copy of the code saved and to be able to collaborate with others.",
            difficulty=DifficultyLevel.intermediate,
            categories=[cat_coding, cat_devops, cat_git, cat_github],
            sources=[src_github]
        )

        term_gitignore = Term(
            slug="gitignore",
            term="Gitignore",
            definition="A .gitignore file is a plain text configuration file in a Git repository that instructs Git which files or directories to ignore and exclude from version control",
            difficulty=DifficultyLevel.advanced,
            categories=[cat_git, cat_github],
            sources=[src_gitignore]
        )

        term_commit = Term(
            slug="commit",
            term="Commit",
            definition="the core building block units of a Git project timeline. Commits can be thought of as snapshots or milestones along the timeline of a Git project. Commits are created with the git commit command to capture the state of a project at that point in time.",
            difficulty=DifficultyLevel.beginner,
            categories=[cat_git, cat_github, cat_commit, cat_coding],
            sources=[src_commit]
        )


        # --- Phase 2: PENDING (Lägg i väntrummet) ---
        # Du behöver bara lägga till termerna. SQLAlchemy är smart nog att se att
        # kategorierna och källorna sitter fast i termerna, så de följer med automatiskt!
        # Steg 4: Lägg till i nuvarande session.
        db.add(term_cicd)
        db.add(term_python)
        db.add(term_git)
        db.add(term_github)
        db.add(term_gitignore)
        db.add(term_commit)

        # --- Phase 3: PERSISTENT (HÄR skickas det till DB för permanent storage) ---
        # Steg 5: Spara(tänk commit i git)
        db.commit()
        print("Data seeded successfully. Check your PgAdmin4!")

        # Steg 6: Verifiera, läs tillbaka(säkertställer paritet)
        # efter db.commit() skickar SQAlchemy ett SELECT statement till postgres via db.scalars(stmt).one()
        # db.scalars(stmt).one() gör alltså en SELECT av sig själv!
            # Om du vill köra EN term och kolla.
            # stmt = select(Term).where(Term.slug == "python")
            # result = db.scalars(stmt).one()

        # Vill du köra FLERA termer, använd detta:
        # Steg 6: Verifiera flera termer (The Batch Way)
        # Vi letar efter alla slugs som finns i vår lista
        slugs_to_find = ["git", "github", "gitignore", "commit"]
        stmt = select(Term).where(Term.slug.in_(slugs_to_find))
        # Använd .all() istället för .one() när du förväntar dig en lista tillbaka
        results = db.scalars(stmt).all()
        for result in results:
            print(f"\n - Verifierar: Hittade termen '{result.term}'")
            print(f"   - Kategorier: {[c.name for c in result.categories]}")
            print(f"   - Sources: {[s.name for s in result.sources]}")
            print(f"-" *20)




    except Exception as e:
        print(f"Error with seeding the data: {e}")
        db.rollback() # <---- Rollback, rullar tillbaka allting om något går fel (Om jag försöker lägga in dubbletter t.ex)
    finally:
        db.close() # <---- VIKTIGT. ALLTID STÄNGA "DÖRREN"

if __name__ == "__main__":
    seed_data()