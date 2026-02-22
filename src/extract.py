# Kod: Engelska
# Kommentarer: Svenska
# För att städa och rensa upp mina glosor och förenkla mitt jobb.
import csv
import os

# 1. Konfig: Vilka filer ska läsas och vad ska de taggas med?

FILES = [
    {"path": "docs/glossary_terms/data_mod_glossary.md", "category": "Data Modeling", "source": "Data Modeling Course"},
    {"path": "docs/glossary_terms/sql_glossary.md", "category": "SQL", "source": "SQL Course"},
    {"path": "docs/glossary_terms/python_glossary.md", "category": "Python", "source": "Python Course"}
]

OUTPUT_FILE = "docs/glossary_raw.csv"

def clean_markdown_files():
    print("Starting to clean messy glossary files (EXTRACT & TRANSFORM)")

    extracted_terms = []
    
    for file_info in FILES:
        filepath = file_info["path"]
        category = file_info["category"]
        source = file_info["source"]

        # Kontroll om filen finns eller inte
        if not os.path.exists(filepath):
            print(f"Cant find file: {filepath}, skipping...")
            continue

        with open(filepath, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip() # leading och trailing whitespaces
                
                # hoppa över helt toppa rader eller avskiljare
                if not line or line.startswith('##') or '---' in line:
                    continue

                term = ""
                definition = ""
                # --- LOGIK 1: Tabell-format (t.ex. "| CRUD | Create Read Update Delete") ---
                if line.startswith('|'):
                    parts = line.split('|')
                    if len(parts) >= 2:
                        term = parts[1].strip()
                        # Om det finns en förklaring i nästa kolumn
                        if len(parts) >= 3:
                            definition = parts[2].strip()
                            # Ignorera rader som bara är rubrikerna i tabellen
                    if term.lower() in ['terminology', 'glossary', 'meaning', 'explanation']:
                        continue
                        
                # --- LOGIK 2: Bindestreck-format (t.ex. "backup - en extra kopia" eller "* git - versionshantering") ---
                elif ' - ' in line:
                    # Ta bort eventuella punktlista-stjärnor (* ) i början
                    clean_line = line.lstrip('* ').strip()
                    parts = clean_line.split(' - ', 1) # Dela BARA på första bindestrecket
                    if len(parts) == 2:
                        term = parts[0].strip()
                        definition = parts[1].strip()

                # --- LOAD: Spara undan termen om vi hittade någon ---
                if term:
                    extracted_terms.append({
                        "Term": term,
                        "Definition": definition,
                        "Category": category,
                        "Source": source,
                        "Difficulty": "beginner" # Jag sätter en default som jag kan ändra sen
                    })
                    
    # 2. Skapa den slutgiltiga CSV-filen
    if extracted_terms:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Term", "Definition", "Category", "Source", "Difficulty"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in extracted_terms:
                writer.writerow(item)
                
        print(f"Klart! Extraherade {len(extracted_terms)} glosor till '{OUTPUT_FILE}'.")
    else:
        print("Hittade inga glosor att extrahera.")

if __name__ == "__main__":
    clean_markdown_files()

