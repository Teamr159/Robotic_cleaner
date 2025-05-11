
Simulace robotického vysavače s využitím umělé inteligence

Tento projekt simuluje chování autonomního robotického vysavače v prostředí s překážkami. Robot nejprve samostatně zmapuje místnost pomocí senzorů a následně ji systematicky uklidí ve stylu hry Snake, přičemž k plánování trasy používá A* algoritmus.

Funkce:
- Mapování místnosti pomocí principu frontier-based exploration.
- Dva kruhové senzory (menší = přesný, větší = orientační).
- Automatické přepnutí do režimu úklidu po dokončení mapy.
- Systematický úklid prostoru pomocí A* (nahoru a dolů jako Snake).
- Vizualizace ve dvou pohledech:
  - Levá část: reálná mapa místnosti, včetně trasy robota.
  - Pravá část: robotův senzorový pohled (pouze co opravdu vidí).

Složky a soubory:
- main.py – hlavní spouštěcí soubor simulace
- robot.py – logika robota, chování v obou režimech
- room.py – reprezentace místnosti, včetně známé a neznámé mapy
- utils.py – pomocné funkce (vzdálenost, generování, A*)
- visualization.py – vykreslení obou pohledů
- settings.py – nastavení (barvy, rychlosti, rozměry)

Spuštění:
1. Ujisti se, že máš nainstalovaný Python 3 a knihovnu pygame:
   pip install pygame

2. Stáhni nebo naklonuj tento projekt.

3. Spusť simulaci pomocí:
   python main.py

Nejčastější problémy:
- Chyba "ModuleNotFoundError: No module named 'pygame'"
  → Nainstaluj pygame příkazem pip install pygame.

- Program nefunguje ve VS Code
  → Zkontroluj, že používáš správný Python interpreter (vpravo dole ve VS Code).

- Okno se okamžitě zavře
  → Spusť program z příkazového řádku (cmd), abys viděl případné chybové hlášení.

Licence:
Tento projekt je vytvořen jako školní (maturitní) projekt a může být dále volně upravován pro studijní účely.
