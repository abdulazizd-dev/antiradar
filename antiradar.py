import time
import pygame
import math
import sys
from geopy.distance import geodesic

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN) 

pygame.display.set_caption("GPS Antiradar Tizimi")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
DARK_GREEN = (0, 50, 0)

GREEN = (0, 255, 0)
RED = (255, 0, 0)

CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
MAX_RADIUS = 250

angle = 0
ROTATION_SPEED = 0.04

RADARLAR_BAZASI = [
{"nomi": "Chilonzor Metro yaqinidagi fotoradar", "koordinata": (41.2742, 69.2041), "tezlik_limiti": 70},
{"nomi": "Mustaqillik maydoni chorraha kamerasi", "koordinata": (41.3165, 69.2644), "tezlik_limiti": 70},
{"nomi": "Minor metrosi radari", "koordinata": (41.3329, 69.2811), "tezlik_limiti": 70},
]

MASHINA_TRAYEKTORIYASI = [
    (41.2785, 69.2045),
    (41.2760, 69.2043),
    (41.2745, 69.2041),    
]

joriy_tezlik = 75
nuqta_indeksi = 0
oxirgi_yangilanish = time.time()

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:
                        running = False

            running = False
            pygame.quit()

            sys.exit()

    if time.time() - oxirgi_yangilanish > 3:

        if nuqta_indeksi < len(MASHINA_TRAYEKTORIYASI) - 1:
            nuqta_indeksi += 1

        else:
            nuqta_indeksi = 0

        oxirgi_yangilanish = time.time()

    joriy_gps = MASHINA_TRAYEKTORIYASI[nuqta_indeksi]                   
    print("GPS Antiradar tizimi ishga tushdi...\n")


    radar_topildi = False
    ogohlantirish_matni = "Yo'l ochiq, yaqin atrofda xavf yo'q."
    ekran_rangi = GREEN

    for radar in RADARLAR_BAZASI:

        masofa = geodesic(joriy_gps, radar["koordinata"]).meters

        if masofa <= 500:
                radar_topildi = True

                if joriy_tezlik > radar["tezlik_limiti"]:
                    ogohlantirish_matni = f" "
                    ekran_rangi = RED

                else:
                    ogohlantirish_matni = f"Radar yaqin: {int(masofa)}m | Tezlik me'yorda."
                    ekran_rangi = GREEN

    screen.fill(BLACK)


    for r in range(50, MAX_RADIUS + 1, 50):
                
                pygame.draw.circle(screen, DARK_GREEN, (CENTER_X, CENTER_Y), r, 1)


    pygame.draw.line(screen, DARK_GREEN, (CENTER_X - MAX_RADIUS, CENTER_Y), (CENTER_X + MAX_RADIUS, CENTER_Y), 1)

    pygame.draw.line(screen, DARK_GREEN, (CENTER_X - MAX_RADIUS*0.7, CENTER_Y - MAX_RADIUS*0.7), (CENTER_X + MAX_RADIUS*0.7, CENTER_Y + MAX_RADIUS*0.7), 1)
    pygame.draw.line(screen, DARK_GREEN, (CENTER_X - MAX_RADIUS*0.7, CENTER_Y + MAX_RADIUS*0.7), (CENTER_X + MAX_RADIUS*0.7, CENTER_Y - MAX_RADIUS*0.7), 1)

    offset = MAX_RADIUS + 20
    pygame.draw.lines(screen, DARK_GREEN, False, [(CENTER_X - offset, CENTER_Y - offset + 15), (CENTER_X - offset, CENTER_Y - offset), (CENTER_X - offset + 15, CENTER_Y - offset)], 2)    
    pygame.draw.lines(screen, DARK_GREEN, False, [(CENTER_X + offset, CENTER_Y - offset + 15), (CENTER_X + offset, CENTER_Y - offset), (CENTER_X + offset - 15, CENTER_Y - offset)], 2)
    pygame.draw.lines(screen, DARK_GREEN, False, [(CENTER_X - offset, CENTER_Y + offset - 15), (CENTER_X - offset, CENTER_Y + offset), (CENTER_X - offset + 15, CENTER_Y + offset)], 2) 
    pygame.draw.lines(screen, DARK_GREEN, False, [(CENTER_X + offset, CENTER_Y + offset - 15), (CENTER_X + offset, CENTER_Y + offset), (CENTER_X + offset - 15, CENTER_Y + offset)], 2)

    pygame.draw.line(screen, DARK_GREEN, (CENTER_X, CENTER_Y - MAX_RADIUS), (CENTER_X, CENTER_Y + MAX_RADIUS), 1)

    for i in range(25):
                
                trail_angle = angle - (i * 0.02)

                end_x = CENTER_X + MAX_RADIUS * math.cos(trail_angle)
                end_y = CENTER_Y + MAX_RADIUS * math.sin(trail_angle)

                alpha = max(0, 255 - (i * 10))

                pygame.draw.line(screen, (0, 255, 0), (CENTER_X, CENTER_Y), (end_x, end_y), 4)

    if radar_topildi and int(time.time() * 2) % 2 ==0:
                
                pygame.draw.circle(screen, RED, (CENTER_X, CENTER_Y), 12)

    title = pygame .font.SysFont("Consolas", 28, bold=True)
    title_surface = title.render("   GPS ANTIRADAR", True, GREEN)
    screen.blit(title_surface, (150, 5))            

    font = pygame.font.SysFont("Consolas", 18)
    text_surface = font.render(ogohlantirish_matni, True, ekran_rangi)
    screen.blit(text_surface, (20, 20))

    speed_surface = font.render(f"Speed: 0 km/h", True, GREEN)
    screen.blit(speed_surface, (20, 520))

    gps_surface = font.render(f"Joriy GPS: {joriy_gps}", True, GREEN)
    screen.blit(gps_surface, (20, 550))

    angle += ROTATION_SPEED
    pygame.display.flip()

    clock.tick(60)