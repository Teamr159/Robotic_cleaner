# Načtení knihovny Pygame a dalších modulů
import pygame
from settings import WIDTH, HEIGHT, FPS        # Import rozměrů okna a FPS z nastavení
from robot import Robot                         # Import třídy robot
from room import Room                           # Import třídy místnosti
from visualization import draw_views            # Funkce pro vykreslení simulace

# Inicializace Pygame
pygame.init()

# Vytvoření okna s danou šířkou a výškou
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Vacuum Cleaner")  # Název okna
clock = pygame.time.Clock()                      # Hodiny pro regulaci FPS

# Vytvoření instance místnosti a robota
room = Room()
robot = Robot(room)

# Hlavní smyčka programu
running = True
while running:
    # Zpracování událostí (např. kliknutí na křížek)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Ukončit smyčku

    # Aktualizace stavu robota (pohyb, rozhodování)
    robot.update()

    # Vyčištění obrazovky (bílá barva na pozadí)
    screen.fill((255, 255, 255))

    # Vykreslení obou pohledů simulace
    draw_views(screen, robot, room)

    # Aktualizace celé obrazovky
    pygame.display.flip()

    # Zpomalení smyčky podle nastaveného FPS
    clock.tick(FPS)

# Ukončení Pygame při zavření simulace
pygame.quit()
