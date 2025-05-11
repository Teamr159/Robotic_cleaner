# Importy knihoven a modulů
import math
import pygame
import random
from settings import CELL_SIZE, SENSOR_RADIUS, EXPLORED_RADIUS, ROBOT_RADIUS, MOVE_SPEED
from utils import find_free_spot, a_star

# Definice třídy Robot, která řídí chování robota
class Robot:
    def __init__(self, room):
        self.room = room                                      # Odkaz na místnost, ve které se robot pohybuje
        self.x, self.y = find_free_spot(self.room.grid)       # Náhodně zvolené volné místo pro start
        self.angle = 0                                        # Úhel otočení (momentálně nevyužit)
        self.mode = "mapping"                                 # Počáteční režim – mapování
        self.cleaned = set()                                  # Množina již vyčištěných dlaždic
        self.path = []                                        # Aktuální naplánovaná cesta (seznam bodů)
        self.trail = []                                       # Historie pohybu (pro vizualizaci)
        self.clean_targets = []                               # Seznam míst, která je potřeba uklidit
        self.clean_path_ready = False                         # Zda již byl vygenerován seznam pro úklid
        self.done = False                                     # Zda je úklid zcela dokončen

    def get_pos(self):
        # Vrací aktuální pozici robota v pixelech (celá čísla)
        return int(self.x), int(self.y)

    def sensor_scan(self):
        # Simulace senzorů – kontroluje body v dosahu obou kruhů
        px, py = self.get_pos()
        for dy in range(-SENSOR_RADIUS, SENSOR_RADIUS + 1):
            for dx in range(-SENSOR_RADIUS, SENSOR_RADIUS + 1):
                tx, ty = px + dx, py + dy
                if 0 <= tx < self.room.pixel_width and 0 <= ty < self.room.pixel_height:
                    dist = math.hypot(dx, dy)
                    if dist <= SENSOR_RADIUS and self.room.line_of_sight((px, py), (tx, ty)):
                        if dist <= EXPLORED_RADIUS:
                            self.room.mark_visible(tx, ty)    # Bod byl skutečně viděn v menším kruhu
                        else:
                            self.room.mark_outer(tx, ty)      # Bod jen v dosahu většího kruhu
        self.trail.append((int(self.x), int(self.y), self.mode))  # Uložení stopy robota

    def move(self, dx, dy):
        # Pokus o posun robota – nejprve zkontroluje kolizi
        new_x = self.x + dx
        new_y = self.y + dy
        if not self.room.collides_pixel(new_x, new_y):
            self.x = new_x
            self.y = new_y

    def update(self):
        # Hlavní logika robota – volána v každém kroku simulace
        self.sensor_scan()

        if self.mode == "mapping":
            if self.room.is_fully_mapped():
                print("✅ Mapa hotová. Přepínám do režimu 'cleaning'")
                self.mode = "cleaning"
                self.path = []
                self.clean_targets = []
                self.clean_path_ready = False
            else:
                self.mapping_behavior()
        elif self.mode == "cleaning":
            if not self.clean_path_ready:
                self.generate_cleaning_targets()
                self.clean_path_ready = True
            self.cleaning_behavior()

    def mapping_behavior(self):
        # Chování při mapování – hledání frontierů a přesun k nim
        cx, cy = int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)
        if not self.path:
            frontier = self.room.find_frontier()
            if frontier:
                self.path = a_star(self.room.grid, (cx, cy), frontier)
        if self.path:
            tx, ty = self.path[0]
            tx_pix = tx * CELL_SIZE + CELL_SIZE // 2
            ty_pix = ty * CELL_SIZE + CELL_SIZE // 2
            dx = tx_pix - self.x
            dy = ty_pix - self.y
            dist = math.hypot(dx, dy)
            if dist < 1.5:
                self.path.pop(0)  # Cíl dosažen
            else:
                angle = math.atan2(dy, dx)
                self.move(math.cos(angle) * MOVE_SPEED, math.sin(angle) * MOVE_SPEED)
        else:
            self.angle += random.choice([90, -90])  # Pokud není cesta, náhodně změní směr

    def generate_cleaning_targets(self):
        # Vygenerování pořadí úklidu – ve stylu Snake (řádek po řádku)
        print("🔄 Generuji seznam úklidových bodů...")
        for y in range(self.room.grid_height):
            row = range(self.room.grid_width) if y % 2 == 0 else reversed(range(self.room.grid_width))
            for x in row:
                if self.room.known[y][x] == 0 and self.room.grid[y][x] == 0:
                    self.clean_targets.append((x, y))
        print(f"🧹 Cílů k úklidu: {len(self.clean_targets)}")

    def cleaning_behavior(self):
        # Chování robota při úklidu
        cx, cy = int(self.x // CELL_SIZE), int(self.y // CELL_SIZE)
        self.cleaned.add((cx, cy))  # Označí současnou buňku jako vyčištěnou

        if not self.path and self.clean_targets:
            # Pokud není aktivní cesta a zbývá cíl, naplánuj trasu
            next_target = self.clean_targets.pop(0)
            start = (int(self.x // CELL_SIZE), int(self.y // CELL_SIZE))
            self.path = a_star(self.room.grid, start, next_target)
            if not self.path:
                print(f"⚠️ Nelze dojít k cíli {next_target}, přeskočeno.")

        if self.path:
            # Pohyb podél naplánované trasy
            tx, ty = self.path[0]
            tx_pix = tx * CELL_SIZE + CELL_SIZE // 2
            ty_pix = ty * CELL_SIZE + CELL_SIZE // 2
            dx = tx_pix - self.x
            dy = ty_pix - self.y
            dist = math.hypot(dx, dy)
            if dist < 1.5:
                self.path.pop(0)  # Cíl dosažen
            else:
                angle = math.atan2(dy, dx)
                self.move(math.cos(angle) * MOVE_SPEED, math.sin(angle) * MOVE_SPEED)
        elif not self.clean_targets and not self.done:
            # Vše uklizeno – úklid dokončen
            print("✅ Úklid dokončen.")
            self.done = True
