# Kod: Engelska
# Kommentarer: Svenska
# För att skapa mina tabeller.
import enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

# --- 0. Enums (Valbara alternativ) ---
# Detta motsvarar min CHECK (difficulty IN (...)) i SQL
class DifficultyLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


# --- 1. Association Tables (Junction Tables) ---
# I SQLAlchemy definieras ofta dessa som variabler istället för klasser,
# eftersom de oftast bara innehåller två ForeignKeys och ingen egen data.
# Motsvarar min: CREATE TABLE term_categories
term_categories = Table(
    "term_categories",
    Base.metadata,
    Column("term_id", Integer, ForeignKey("terms.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

# Motsvarar min: CREATE TABLE term_sources
term_sources = Table(
    "term_sources",
    Base.metadata,
    Column("term_id", Integer, ForeignKey("terms.id", ondelete="CASCADE"), primary_key=True),
    Column("source_id", Integer, ForeignKey("sources.id", ondelete="CASCADE"), primary_key=True),
)

# --- 2. Main Models (Entiteter) ---

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # Relation: En kategori har många terms.
    # 'secondary' pekar på junction-tabellen jag skapade ovan.
    terms = relationship("Term", secondary=term_categories, back_populates="categories")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"
    

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    source_type = Column(String(50)) # T.ex. 'book', 'video'
    url = Column(Text, nullable=True)

    # Relation: En source har många terms kopplade till sig
    terms = relationship("Term", secondary=term_sources, back_populates="sources")

    def __repr__(self):
        return f"<Source(name='{self.name}')>"
    

class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True) # URL-vänligt namn
    term = Column(String(100), unique=True, nullable=False) # Riktiga namnet
    definition = Column(Text, nullable=False)
    example = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Här använder jag min Enum-klass!
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.beginner)

    # Tidsstämplar (server_default=func.now() låter databasen sätta tiden)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # --- THE GLUE (Relationerna) ---
    # Detta skapar inga kolumner i databasen, men det skapar magi i Python.
    # Jag kan nu göra: my_term.categories.append(python_category)
    
    categories = relationship("Category", secondary=term_categories, back_populates="terms")
    sources = relationship("Source", secondary=term_sources, back_populates="terms")

    def __repr__(self):
        return f"<Term(slug='{self.slug}')>"