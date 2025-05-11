import math  # Import matematické knihovny (pro úhly, vzdálenosti atd.)

# ------------------------
# Nastavení rozměrů okna
# ------------------------

WIDTH, HEIGHT = 1200, 600           # Celková velikost okna simulace (šířka, výška v pixelech)
MAP_WIDTH, MAP_HEIGHT = 600, 600    # Velikost mapovací části (pro každé okno zvlášť)
CELL_SIZE = 10                      # Velikost jedné buňky mřížky (v pixelech)

# Počet buněk v mřížce (šířka a výška v počtu buněk)
GRID_WIDTH = MAP_WIDTH // CELL_SIZE
GRID_HEIGHT = MAP_HEIGHT // CELL_SIZE

# ------------------------
# Barvy (RGB)
# ------------------------

WHITE = (255, 255, 255)       # Bílá – pozadí levé mapy
BLACK = (0, 0, 0)             # Černá – zdi a překážky
BLUE = (0, 102, 204)          # Modrá – stopa robota při mapování
GREEN = (0, 255, 0)           # Zelená – stopa robota při úklidu
GREY = (200, 200, 200)        # Šedá – barva robota nebo rastru
LIGHT_GREY = (220, 220, 220)  # Světle šedá – vnější senzorový kruh
DARK_GREY = (50, 50, 50)      # Tmavě šedá – neprozkoumaný prostor v robotově pohledu
RED = (255, 0, 0)             # Červená – (volitelně pro ladění nebo chyby)
YELLOW = (255, 255, 0)        # Žlutá – (volitelně např. pro aktuální cíl)

# ------------------------
# Nastavení robota
# ------------------------

ROBOT_RADIUS = 5             # Poloměr robota (pro kreslení a kolize)
SENSOR_RADIUS = 70           # Větší kruh – maximální dosah senzoru
EXPLORED_RADIUS = 50         # Menší kruh – to, co robot „opravdu vidí“
TURN_SPEED = math.radians(10)  # Rychlost otáčení (aktuálně se nevyužívá)
MOVE_SPEED = 2               # Rychlost pohybu robota (pixely za snímek)

# ------------------------
# Obnovovací frekvence
# ------------------------

FPS = 60  # Počet snímků za sekundu (Frame Per Second)
