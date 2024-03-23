import pygame
import math
pygame.init()

# The world map is represented by a 2D-Array. 
# A one represents a wall-tile and a zero represents a floor tile.
world_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

LINKS = 900
WIN_HEIGHT = 600
WIN_WIDTH = LINKS + WIN_HEIGHT
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
NUMBER_OF_RAYS = int(LINKS / LINE_WIDTH) + 1
FIELD_OF_VIEW = math.radians(50)
ANGLE_BETWEEN_RAYS = FIELD_OF_VIEW / (NUMBER_OF_RAYS - 1)
WALL_SIZE = WIN_HEIGHT * 1.1

screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption('RAYCAST')
clock = pygame.time.Clock()

FPS = 60
BLOCK_SIZE = WIN_HEIGHT / len(world_map)

font = pygame.font.Font(None, 65) # Erstellen Sie ein Font-Objekt mit der Standard-Schriftart und einer Größe von 36
text = font.render('GEWONNEN !!!', True, (200, 200, 0)) # Erstellen Sie ein Text-Objekt

MAX_BRIGHTNESS = 200
DIM_FACTOR = -10

run = True
while run:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Draw background
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 50), (0, 0, LINKS, WIN_HEIGHT / 2))
    pygame.draw.rect(screen, (65, 40, 20), (0, WIN_HEIGHT / 2, LINKS, WIN_HEIGHT / 2))
    
    # Get user input
    keys = pygame.key.get_pressed()
    
    # Move forwards
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


    # The y-position relative to the cell the player is in. (Between 0 and 1)
    cell_y = player_y - math.floor(player_y)
    
    # Set values to calculate the first ray
    ray_direction = alpha + FIELD_OF_VIEW / 2
    ray_direction %= 2 * math.pi
    line_screen_x = 0
    
    # Repeat for every ray
    for i in range(NUMBER_OF_RAYS):
        
        # Cell in which the ray is currently in.
        ray_block_column = int(player_x)
        ray_block_row = int(player_y)
        
        ray_direction_degrees = math.degrees(ray_direction)
        
        if ray_direction_degrees > 0 and ray_direction_degrees < 180:
            # Ray points up
            next_horizontal_intersection_x = player_x + cell_y / math.tan(ray_direction)
            delta_x = 1 / math.tan(ray_direction)
            ray_row_movement = -1
        else:
            # Ray points down
            next_horizontal_intersection_x = player_x - (1 - cell_y) / math.tan(ray_direction)
            delta_x = -1 / math.tan(ray_direction)
            ray_row_movement = 1
        
        if ray_direction_degrees > 270 or ray_direction_degrees < 90:
            # Ray also points right
            next_vertical_intersection_x = math.ceil(player_x)
            ray_column_movement = 1
        else:
            # Ray also points left
            next_vertical_intersection_x = math.floor(player_x)
            ray_column_movement = -1
        
        # Send out the ray until it hits a wall.
        # Calculate the x-coordinates of the rays intersections with the grid.
        while True:
            
            distance_horizontal_intersection = abs(player_x - next_horizontal_intersection_x)
            distance_vertical_intersection = abs(player_x - next_vertical_intersection_x)
            
            if distance_horizontal_intersection < distance_vertical_intersection:
                cur_intersection_x = next_horizontal_intersection_x
                ray_block_row += ray_row_movement
                next_horizontal_intersection_x += delta_x
                shadow = False
            else:
                cur_intersection_x = next_vertical_intersection_x
                ray_block_column += ray_column_movement
                next_vertical_intersection_x += ray_column_movement
                shadow = True
            
            # End the loop if the ray hits a wall.
            if world_map[ray_block_row][ray_block_column] == 1:
                break
        
        # Length of ray
        raw_distance = (cur_intersection_x - player_x) / math.cos(ray_direction)
        distance_without_fisheye = raw_distance * math.cos(ray_direction - alpha)

        # Vertical line on screen
        line_height = WALL_SIZE / distance_without_fisheye
        line_start = (WIN_HEIGHT / 2) - (line_height / 2)
        line_start = max(line_start, 0) # Make sure line_start is not smaller than 0.
        line_end = (WIN_HEIGHT / 2) + (line_height / 2)
        line_end = min(line_end, WIN_HEIGHT) # Make sure line_end is not bigger than WIN_HEIGHT.
        
        # Brightness / color of line (walls that are further away are darker.)
        brightness = int(DIM_FACTOR * distance_without_fisheye + MAX_BRIGHTNESS)
        brightness = max(brightness, 0) # Make sure brightness is not smaller than 0.
        if shadow: brightness //= 2
        color = (0, brightness, 0)
        
        # Draw line
        pygame.draw.line(screen, color, (line_screen_x, line_start), (line_screen_x, line_end), LINE_WIDTH)
        
        # Set values to calculate the next ray.
        ray_direction -= ANGLE_BETWEEN_RAYS
        ray_direction %= 2 * math.pi
        line_screen_x += LINE_WIDTH
    #Draw 2D Weltkarte ----------------------------------------------------------------------------------------------
    for row in range(len(world_map)):
        for column in range(len(world_map[0])):
            block_x = column * BLOCK_SIZE + LINKS
            block_y = row * BLOCK_SIZE
            color = (255,0,0) if world_map[row][column] == 1 else (200,200,200)
            pygame.draw.rect(screen,color,(block_x,block_y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(screen,(10,10,10),(block_x,block_y,BLOCK_SIZE,BLOCK_SIZE),1)

    # Draw Player
    player_screen_x = player_x * BLOCK_SIZE + LINKS
    player_screen_y = player_y * BLOCK_SIZE
    box_screen_x = box_x * BLOCK_SIZE + LINKS
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
