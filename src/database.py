# Kod: Engelska
# Kommentarer: Svenska
# För att sätta upp Engine och Session(Se docs/o)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.config import settings

# 1: Skapa motorn(Engine)
# Den pratar med min docker-container på port 5435
engine = create_engine(settings.DATABASE_URL)

# 2: Skapa SESSION FACTORY
# Den används för att skapa nya sessions för varje call(anrop)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3: Skapa DECLARATIVE BASE
# Alla modeller(tables) kommer ärva från den här
class Base(DeclarativeBase):
    pass

# 4: Dependency(Helper för FastAPI)
# Funktionen ser till att det öppnas en DB session och lånar ut den till endpoint + stänger efter.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()