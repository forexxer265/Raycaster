import pygame
import math
import random
pygame.init()
world_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

WIN_WIDTH = 600
WIN_HEIGHT = 600
RECHTS = WIN_WIDTH / 2

# Starting position and direction of player
player_x = 4.7
player_y = 5.2
MOVE_SPEED = 0.06
ROT_SPEED = math.radians(1)
alpha = math.radians(45)
box_x = 2.5
box_y = 1.6

player_x += 0.0000001
player_y += 0.0000001
alpha += 0.0000001


# Constants for raycasting
LINE_WIDTH = 2
NUMBER_OF_RAYS = int(WIN_WIDTH / LINE_WIDTH) + 1
FIELD_OF_VIEW = math.radians(50)
ANGLE_BETWEEN_RAYS = FIELD_OF_VIEW / (NUMBER_OF_RAYS - 1)
WALL_SIZE = WIN_HEIGHT * 1.1

MAX_BRIGHTNESS = 200
DIM_FACTOR = -10
screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption('RAYCAST')
clock = pygame.time.Clock()

FPS = 60
BLOCK_SIZE = WIN_HEIGHT / len(world_map)

font = pygame.font.Font(None, 65) # Erstellen Sie ein Font-Objekt mit der Standard-Schriftart und einer Größe von 36
text = font.render('GEWONNEN !!!', True, (200, 200, 0)) # Erstellen Sie ein Text-Objekt

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((0,0,0))
    # pygame.draw.rect(screen,(0,0,50),(0,0,WIN_WIDTH / 2, WIN_HEIGHT / 2))
    # pygame.draw.rect(screen,(65,40,20),(0,WIN_HEIGHT / 2,WIN_WIDTH / 2, WIN_HEIGHT))
    #

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        alpha += ROT_SPEED
        alpha %= 2 * math.pi
    if keys[pygame.K_RIGHT]:
        alpha -= ROT_SPEED
        alpha %= 2 * math.pi
    if keys[pygame.K_UP]:
        new_x = player_x + MOVE_SPEED * math.cos(alpha)
        if world_map[int(player_y)][int(new_x)] == 0:
            player_x = new_x
        new_y = player_y - MOVE_SPEED * math.sin(alpha)
        if world_map[int(new_y)][int(player_x)] == 0:
            player_y = new_y
    if keys[pygame.K_DOWN]:
        new_x = player_x - MOVE_SPEED * math.cos(alpha)
        if world_map[int(player_y)][int(new_x)] == 0:
            player_x = new_x
        new_y = player_y + MOVE_SPEED * math.sin(alpha)
        if world_map[int(new_y)][int(player_x)] == 0:
            player_y = new_y


    #Draw 2D Weltkarte ----------------------------------------------------------------------------------------------
    for row in range(len(world_map)):
        for column in range(len(world_map[0])):
            block_x = column * BLOCK_SIZE
            block_y = row * BLOCK_SIZE
            color = (255,0,0) if world_map[row][column] == 1 else (200,200,200)
            pygame.draw.rect(screen,color,(block_x,block_y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(screen,(10,10,10),(block_x,block_y,BLOCK_SIZE,BLOCK_SIZE),1)

    # Draw Player
    player_screen_x = player_x * BLOCK_SIZE
    player_screen_y = player_y * BLOCK_SIZE
    box_screen_x = box_x * BLOCK_SIZE 
    box_screen_y = box_y * BLOCK_SIZE

    pygame.draw.circle(screen, (0, 0, 0), (box_screen_x, box_screen_y), 9)
    pygame.draw.circle(screen, (0, 0, 250), (player_screen_x, player_screen_y), 7)

    # Raycasting
    for i in range(0, 500, 10):
        ray_angle = alpha + math.radians(i - 150) / 60
        ray_x = player_x
        ray_y = player_y
        while world_map[int(ray_y)][int(ray_x)] == 0:
            ray_x += 0.03 * math.cos(ray_angle)
            ray_y -= 0.03 * math.sin(ray_angle)
        distance_to_wall = math.sqrt((ray_x - player_x) ** 2 + (ray_y - player_y) ** 2)
        ray_screen_x = player_screen_x + distance_to_wall * BLOCK_SIZE * math.cos(ray_angle)
        ray_screen_y = player_screen_y - distance_to_wall * BLOCK_SIZE * math.sin(ray_angle)
        pygame.draw.line(screen, (255, 255, 0), (player_screen_x, player_screen_y), (ray_screen_x, ray_screen_y), 3)

    abstand = math.sqrt((player_x - box_x) ** 2 + (player_y - box_y) ** 2)
    if abstand < 0.2:
        screen.blit(text, (WIN_WIDTH // 10, WIN_HEIGHT // 22))  # Zeichnen Sie den Text in der Mitte des Bildschirms
        pygame.display.flip()  # Aktualisieren Sie den Bildschirm, um den Text anzuzeigen
        pygame.time.wait(6000)  # Warten Sie 2 Sekunden (2000 Millisekunden)
        run = False  # Beenden Sie die Hauptschleife, um das Spiel zu stoppen------------------------------------------

    pygame.display.flip()
pygame.display.quit()

