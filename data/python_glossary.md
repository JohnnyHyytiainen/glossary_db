## Glossary python


| terminology
| ---------------
 git   -   versionshanteringssystem, sparar snapshots av varje committad ändring av ditt script.

github    -   versionshantering via git MEN molnbaserad tjänst du pushar dina ändringar till. Används för att ha extra kopia på koden sparad och för att kunna samarbeta med andra.

backup    -   en extra kopia på någonting, används för säkerhet utifall någonting händer, t.ex en fil blir korrupt och ej läsbar. Har du en backup på originalet kan du läsa den istället utan problem.

| gitignore     -   en textfil i root i projektet, tack vare filen kan du skriva och ändra vilka filer du vill spåra med git eller som git ska ignorera, detta för att undvika att känsliga filer ska sparas eller pushas till github.

| commit    -   commit är en operation som sparar ändringar i källkoden permanent i ett arkiv (repository). Det sparar en snapshot på det du arbetar med om någonting råkar gå förlorat eller om du vill gå tillbaka till tidigare version som fungerade.

| pull  -   kommandot git pull används för att hämta och ladda ner innehåll från ett repository och omedelbart uppdatera det lokala arkivet så att det matchar det innehållet.

| clone     -   git clone används för att skapa en lokal kopia av ett befintligt repo (remote repository), till exempel från GitHub, GitLab eller Bitbucket. Det laddar ner hela projektets historik, filer och alla grenar (branches) till din dator, vilket gör att du kan arbeta lokalt och senare synkronisera ändringar.

| cd    -   linux kommando som står för 'change directory'

| ls    -   linux kommando som står för 'list'

| cd ..     -   linux kommando som står för 'change directory bakåt'. Den flyttar dig bakåt en directory.

| data type     -   data type frågar om vad för TYP det är på datan. Heltal(integer), decimaler(float), text(string), Sant/Falskt(Boolean). Notera att det är stor skillnad på Data type och Data structure.

| data structure    -   Data structures är ett sätt att organisera, lagra och hantera data för att kunna använda den effektivt. Exempel på datastruktur är, list [], tuple (), dictionary {}.

| variable      -   en variabel är som en behållare som du ger ett namn och ett värde, till exempel hw = 'Hello World'. Då kan du kalla på variabeln när som helst med hw istället för att skriva Hello World.

| assignment    -   en tilldelning enkelt förklarat. Har du en variabel = 10 så innebär det att likhetstecknet tilldelar variabeln 10 (som är en int i detta exempel).

| input     -   input är det som går in.

| output    -   output är det som kommer ut.

| type casting  -   innebär att en variabel av en viss datatyp konverteras till en annan. Till exempel: x = int(11.7), detta kommer bli 12 pga int är heltal och ej decimaler. https://www.w3schools.com/python/python_casting.asp

| boolean   -   en bool är True eller False. If x = True, ... ... True är här en bool.

| string    -   en string kännetecknas av 'text'


| indentation


| convention
|
| terminology
| ---------------------
| control structures
| conditional statement
| if
| elif
| else
| for
| while
| break
| continue
| boolean expression
| loop
| nested loop
| nested if statement
| expression
| statement
| control flow
|
| terminology
| --------------- 
| sequence
| list
| tuple
| set
| range
| indexing
| slicing
| comprehension
| zip
| enumermate
| unpacking
| membership test
|
| terminology
| ------------------
| replace
| regular expression 
| concatenation
| split
| indexing
| escape charactrers
| unicode
| exception
| try block
| except block
| finally block
| traceback
| open()
| with
| context manager
| close()
|
| terminology
| -------------------- 
| def
| function call
| argument
| return statement
| parameter
| default parameter
| keyword arguments
| variable arguments
| positional arguments
| lambda functions
| dict()
| get()
| items()
| in operator
| del
| update()
|
| terminology
|------------------ 
| class
| object
| instance
| encapsulation
| private
| property
| validation
| abstraction
| polymorphism
| method overloading
| inheritance
| composition
| base class
| superclass
| parent
| child
| unit test
| assertion
| test coverage
| TDD