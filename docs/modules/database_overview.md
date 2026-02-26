
### 1. `Category` (Taggarna / Pärmarna) 

Det här är mina breda ämnesområden. De finns till för att Jag i framtiden ska kunna filtrera fram "Visa mig allt jag kan om SQL".

* **Vad som ska in här:** Övergripande koncept.
* **Kolumner i koden:** `name` och `description`.
* **Exempel:** `"SQL"`, `"Data Modeling"`, `"Python"`, `"DevOps"`.

---

### 2. `Source` (Kvittot / Ursprunget) 

Här sparar jag exakt *varifrån* du fick informationen. Det gör att jag slipper skriva samma källa 50 gånger i mina anteckningar, och du kan enkelt uppdatera länkar om en kurs byter plattform.

* **Vad som ska in här:** Kurser, böcker, dokumentation, YouTube-kanaler.

* **Kolumner i koden:** `name`, `source_type` (t.ex. "Course" eller "Docs"), och `url`.

* **Exempel:** `"DE 25 Programmering"`, `"PostgreSQL Official Docs"`.

---

### 3. `Term` (Själva Gloskortet)

Det här är hjärtat i databasen. Allt mitt faktiska pluggmaterial landar här.

- **Vad som ska in här:** Det specifika ordet, förklaring av det, och hur svårt det är.

- **Kolumner i koden:**  `term`: Det snygga namnet (t.ex `"Primary Key"`).

* `slug`: Datorns/URL:ens namn (t.ex `"primary-key"`). Små bokstäver, bindestreck istället för mellanslag.

* `definition`: Förklaring av glosan.

* `difficulty`: Nybörjare, mellan eller avancerad (via  `DifficultyLevel` Enum).

* `notes` & `example`: *(Valfritt)* Mina personliga minnesregler eller kodexempel.



---

### Hur de pratar med varandra

När Jag skriver in en `Term` i min Python-kod (i `seed.py`), plockar jag helt enkelt upp de `Category` och `Source`-objektet som redan är skapat och "fäster" dem på termen, så här:  
`categories=[min_sql_kategori], sources=[min_kurs_källa]`

---