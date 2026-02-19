# Theory to better understand an objects lifecycle in SQLAlchemy

## The three phases: 
```text
Teori: Ett objekts livscykel i SQLAlchemy

När du skapar data i Python och sparar det till databasen går objektet igenom tre faser. Detta är extremt viktigt att förstå.

1: Transient (Tillfällig): När du skriver cat = Category(name="DevOps"). Objektet finns bara i din dators RAM-minne. Databasen vet ingenting.

2: Pending (I väntrummet): När du skriver db.add(cat). Nu har du lagt objektet i Sessionens (brickans) väntrum. Fortfarande inget i databasen.

3: Persistent (Sparad): När du skriver db.commit(). Nu skickar SQLAlchemy en INSERT INTO-query till Postgres. Objektet är nu permanent sparat och har fått ett riktigt id från databasen.
```

## Example before seed(after revision and migration only) and after seed.
**Before seeding**
```text
FÖRE SEED (Verifiera strukturen):

1: Gå till din databas glossary_db -> Schemas -> public -> Tables.

2: Högerklicka på tabellen terms -> View/Edit Data -> All Rows. Den ska vara helt tom.

3: Titta på tabellen term_categories (din junction table). Tom den med.
```
**After seeding**
```text
EFTER SEED (Verifiera magin):

1: När skriptet har kört, uppdatera vyn för terms. Du bör nu se dina glosor med autogenererade ID:n.

2: Titta på term_categories. Här är magin: Du kommer se siffror (t.ex. term_id: 1, category_id: 1). Du har aldrig sagt åt Python att skriva in just de siffrorna, SQLAlchemy räknade ut det åt dig baserat på relationerna!
```