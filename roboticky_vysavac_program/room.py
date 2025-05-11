# Import potřebných knihoven a nastavení
import pygame
from settings import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE
from utils import generate_room, line_of_sight

# Třída Room reprezentuje celou místnost, včetně překážek a mapy známého prostoru
class Room:
    def __init__(self):
        self.grid = generate_room()  # Vygeneruje mřížku místnosti s překážkami a zdmi (0 = volno, 1 = překážka)
        self.grid_width = GRID_WIDTH
        self.grid_height = GRID_HEIGHT
        self.pixel_width = self.grid_width * CELL_SIZE    # Šířka místnosti v pixelech
        self.pixel_height = self.grid_height * CELL_SIZE  # Výška místnosti v pixelech

        # Matice známého prostředí – výchozí hodnota -1 (neznámé)
        # 0 = volný prostor (viděný menším senzorem)
        # 1 = překážka
        # 2 = šedý okraj – prostor, který byl ve větším kruhu, ale ještě nebyl detailně prozkoumán
        self.known = [[-1 for _ in range(self.grid_width)] for _ in range(self.grid_height)]

    def map_from_pixels(self, px, py):
        # Převede souřadnice v pixelech na souřadnice v mřížce a vrátí hodnotu mřížky (0 = volno, 1 = překážka)
        gx = int(px // CELL_SIZE)
        gy = int(py // CELL_SIZE)
        if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
            return self.grid[gy][gx]
        return 1  # mimo hranice = překážka

    def mark_visible(self, px, py):
        # Označí bod jako prozkoumaný – tedy viděný menším senzorem
        gx = int(px // CELL_SIZE)
        gy = int(py // CELL_SIZE)
        if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
            self.known[gy][gx] = 0

    def mark_obstacle(self, px, py):
        # Označí bod jako překážku (tuto metodu lze volat ručně, ale robot překážky pozná nepřímo)
        gx = int(px // CELL_SIZE)
        gy = int(py // CELL_SIZE)
        if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
            self.known[gy][gx] = 1

    def mark_outer(self, px, py):
        # Označí bod jako „vnějšek“ – tedy viděný ve větším kruhu, ale ještě ne v menším
        gx = int(px // CELL_SIZE)
        gy = int(py // CELL_SIZE)
        if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
            if self.known[gy][gx] == -1:
                self.known[gy][gx] = 2  # světle šedý okraj

    def collides_pixel(self, px, py):
        # Zjistí, zda je na daném pixelu překážka (pro účely pohybu robota)
        return self.map_from_pixels(px, py) == 1

    def line_of_sight(self, a, b):
        # Zjistí, zda je mezi body 'a' a 'b' přímá viditelnost (neblokovaná překážkou)
        return line_of_sight(self.grid, a[0] // CELL_SIZE, a[1] // CELL_SIZE, b[0] // CELL_SIZE, b[1] // CELL_SIZE)

    def is_fully_mapped(self):
        # Vrací True, pokud už nejsou žádné frontier body – tedy místnost je celá zmapovaná
        return self.find_frontier() is None

    def find_frontier(self):
        # Hledá první bod, který je na hranici známého a neznámého prostoru
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.known[y][x] == 2:  # šedý okraj
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                                if self.known[ny][nx] == -1:  # soused je neznámý = validní frontier
                                    return (x, y)
        return None  # žádný frontier nenalezen
