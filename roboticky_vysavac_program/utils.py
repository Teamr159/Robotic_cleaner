import math       # Matematické funkce (např. vzdálenosti)
import random     # Pro generování náhodných překážek
from settings import GRID_WIDTH, GRID_HEIGHT, CELL_SIZE  # Rozměry mřížky

# Výpočet Eukleidovské vzdálenosti mezi dvěma body (pixely)
def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# Heuristika pro A* – v tomto případě je to právě vzdálenost
def heuristic(a, b):
    return distance(a, b)

# Zjišťuje, zda existuje přímá viditelnost (bez překážek) mezi dvěma body v mřížce
def line_of_sight(grid, x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    n = 1 + dx + dy
    x_inc = 1 if x1 > x0 else -1
    y_inc = 1 if y1 > y0 else -1
    error = dx - dy
    dx *= 2
    dy *= 2

    for _ in range(n):
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            if grid[y][x] == 1:  # Překážka zamezuje viditelnosti
                return False
        if error > 0:
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx
    return True

# Generuje náhodnou místnost s vnějšími zdmi a překážkami uvnitř
def generate_room():
    room_map = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Vnější zdi
    for x in range(GRID_WIDTH):
        room_map[0][x] = 1
        room_map[GRID_HEIGHT - 1][x] = 1
    for y in range(GRID_HEIGHT):
        room_map[y][0] = 1
        room_map[y][GRID_WIDTH - 1] = 1

    # Náhodně přidané překážky – obdélníky, čáry a L-tvary
    for _ in range(15):
        shape_type = random.choice(['rect', 'line', 'L'])
        rx = random.randint(2, GRID_WIDTH - 8)
        ry = random.randint(2, GRID_HEIGHT - 8)

        if shape_type == 'rect':
            rw, rh = random.randint(3, 6), random.randint(3, 6)
            for y in range(ry, ry + rh):
                for x in range(rx, rx + rw):
                    room_map[y][x] = 1
        elif shape_type == 'line':
            horizontal = random.choice([True, False])
            length = random.randint(4, 8)
            if horizontal:
                for i in range(length):
                    room_map[ry][rx + i] = 1
            else:
                for i in range(length):
                    room_map[ry + i][rx] = 1
        elif shape_type == 'L':
            for i in range(4):
                room_map[ry + i][rx] = 1
                room_map[ry + 3][rx + i] = 1

    return room_map

# Najde náhodné volné místo v místnosti (mimo překážky, s minimálním odstupem)
def find_free_spot(room_map, min_clearance=2):
    while True:
        x = random.randint(min_clearance, GRID_WIDTH - min_clearance - 1)
        y = random.randint(min_clearance, GRID_HEIGHT - min_clearance - 1)
        clear = True
        for dy in range(-min_clearance, min_clearance + 1):
            for dx in range(-min_clearance, min_clearance + 1):
                if room_map[y + dy][x + dx] == 1:
                    clear = False
        if clear:
            return x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2

# --- A* algoritmus pro hledání nejkratší cesty ---
import heapq  # Prioritní fronta

def a_star(grid, start, goal):
    def neighbors(pos):
        x, y = pos
        results = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        # Vrací pouze volné sousedy v rámci mřížky
        return [(nx, ny) for nx, ny in results
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[ny][nx] != 1]

    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, []))  # f, g, pozice, cesta
    visited = set()

    while open_set:
        f, cost, current, path = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)
        path = path + [current]

        if current == goal:
            return path[1:]  # Vrací cestu bez startovní pozice

        for neighbor in neighbors(current):
            if neighbor not in visited:
                g = cost + 1
                f = g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, g, neighbor, path))

    return []  # Pokud cesta neexistuje
