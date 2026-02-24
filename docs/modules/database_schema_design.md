## Ideas on how to design my glossary database and db tables

```sql
-- Core terms table
CREATE TABLE terms (
    term_id SERIAL PRIMARY KEY,
    term VARCHAR(100) NOT NULL UNIQUE,
    definition TEXT NOT NULL,
    example TEXT,
    notes TEXT,  -- personal notes etc
    difficulty VARCHAR(20) CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories (normalized!)
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Many-to-many junction (like YrkesCo lab)
CREATE TABLE term_categories (
    term_id INTEGER REFERENCES terms(term_id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(category_id) ON DELETE CASCADE,
    PRIMARY KEY (term_id, category_id)
);

-- Sources (track where I learned it!)
CREATE TABLE sources (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL UNIQUE,
    source_type VARCHAR(50),  -- 'course', 'book', 'article', 'video'
    url TEXT
);

-- Link terms to sources (cool to have the sources)
CREATE TABLE term_sources (
    term_id INTEGER REFERENCES terms(term_id) ON DELETE CASCADE,
    source_id INTEGER REFERENCES sources(source_id) ON DELETE CASCADE,
    PRIMARY KEY (term_id, source_id)
);

```