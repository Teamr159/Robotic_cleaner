import pygame
from settings import MAP_WIDTH, CELL_SIZE, BLACK, GREEN, WHITE, RED, DARK_GREY, LIGHT_GREY, ROBOT_RADIUS

# Funkce vykreslí dvě části simulace: 
# 1) vlevo "boží pohled" na mapu místnosti
# 2) vpravo robotův subjektivní pohled
def draw_views(screen, robot, room):
    rx, ry = robot.get_pos()  # Souřadnice robota v pixelech

    # === LEVÁ ČÁST: úplná mapa místnosti ===
    map_view = pygame.Surface((MAP_WIDTH, room.pixel_height))  # Nový povrch pro levou mapu
    map_view.fill(WHITE)  # Pozadí je bílé

    # Vykreslení pevných překážek (zdi, nábytek) z originální mapy
    for y in range(room.grid_height):
        for x in range(room.grid_width):
            px = x * CELL_SIZE
            py = y * CELL_SIZE
            if room.grid[y][x] == 1:
                pygame.draw.rect(map_view, BLACK, (px, py, CELL_SIZE, CELL_SIZE))

    # Vykreslení trasy robota (modrá při mapování, zelená při úklidu)
    for i in range(1, len(robot.trail)):
        x1, y1, mode1 = robot.trail[i - 1]
        x2, y2, mode2 = robot.trail[i]
        color = (0, 102, 204) if mode2 == "mapping" else GREEN  # Barva podle režimu
        pygame.draw.line(map_view, color, (x1, y1), (x2, y2), 2 * ROBOT_RADIUS)  # Tloušťka odpovídá průměru robota

    # Vykreslení samotného robota (červený kruh)
    pygame.draw.circle(map_view, RED, (int(rx), int(ry)), ROBOT_RADIUS)

    # Umístění mapy na levou polovinu obrazovky
    screen.blit(map_view, (0, 0))

    # === PRAVÁ ČÁST: pohled robota podle jeho senzorů ===
    pov_view = pygame.Surface((MAP_WIDTH, room.pixel_height))  # Nový povrch pro robotův pohled
    pov_view.fill(DARK_GREY)  # Tmavě šedé pozadí symbolizuje neprozkoumané oblasti

    for y in range(room.grid_height):
        for x in range(room.grid_width):
            state = room.known[y][x]  # Informace o tom, co už robot „ví“
            rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if state == 1:
                pygame.draw.rect(pov_view, BLACK, rect)        # Překážka
            elif state == 0:
                pygame.draw.rect(pov_view, WHITE, rect)        # Detailně prozkoumaný prostor
            elif state == 2:
                pygame.draw.rect(pov_view, LIGHT_GREY, rect)   # Okraj většího kruhu – jen zhruba viděné místo

    # Robot v pohledu robota – červený kruh na aktuální pozici
    pygame.draw.circle(pov_view, RED, (int(rx), int(ry)), ROBOT_RADIUS)

    # Umístění robotova pohledu na pravou polovinu obrazovky
    screen.blit(pov_view, (MAP_WIDTH, 0))
