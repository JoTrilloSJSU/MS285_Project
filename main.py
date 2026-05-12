#Code has bee modified form below:
# Créé par Administrateur, le 23/05/2025 en Python 3.7
# https://github.com/Gruikjr/webol

import pygame
import random
import sys
import os

pygame.init()

#constants
TILE_SIZE = 32
WORLD_WIDTH = 31
WORLD_HEIGHT = 31
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BEACH_START_X = 700

# Colors
WATER = (52, 101, 164)
HUD_BG = (30, 30, 60)
HUD_TEXT = (255, 255, 255)

# Tile types 0 = water 1 = rock obstacle
TILE_TYPES = [0, 1]

# Coin types 0 = sardine 1 = anchovy
COIN_TYPES = [0, 1]

pygame.display.set_caption("Sea Lion Game")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# Backgrounds
water_bg = pygame.image.load("assets/sprites/water.png").convert()
beach_bg = pygame.image.load("assets/sprites/beach.png").convert_alpha()
WORLD_PIXEL_WIDTH = WORLD_WIDTH * TILE_SIZE
WORLD_PIXEL_HEIGHT = WORLD_HEIGHT * TILE_SIZE
water_bg = pygame.transform.scale(water_bg,(WORLD_PIXEL_WIDTH, WORLD_PIXEL_HEIGHT))
beach_bg = pygame.transform.scale(beach_bg,(WORLD_PIXEL_WIDTH, WORLD_PIXEL_HEIGHT))

# Obstacles and coins
rock_img = pygame.image.load("assets/sprites/rock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img, (32, 32))
coin_img = pygame.image.load("assets/sprites/fish.png").convert_alpha()
coin_img2 = pygame.image.load("assets/sprites/fish2.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (28, 28))
coin_img2 = pygame.transform.scale(coin_img2, (28, 28))

# Player animation frames
player_frames = []

for i in range(4):
    img = pygame.image.load( f"assets/sprites/sealion-frames/pixil-frame-{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (48, 48))
    player_frames.append(img)

#sound
try:
    coin_sound = pygame.mixer.Sound(file=None)
except:
    coin_sound = None



def draw_text(surface, text, pos, color):
    img = font.render(text, True, color)
    surface.blit(img, pos)


def generate_world(): #note: use AI to help with this function
    world = []
    for y in range(WORLD_HEIGHT):
        row = []
        for x in range(WORLD_WIDTH):  
            pixel_x = x * TILE_SIZE
            # No rocks on beach
            if pixel_x >= BEACH_START_X:
                t = 0
            else:        
                t = random.choices(TILE_TYPES,weights=[20, 1])[0]
            row.append(t)
        world.append(row)
    return world

def place_coins(world, n):
    coins = {}
    while len(coins) < n:

        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)

        pixel_x = x * TILE_SIZE

        # Only place fish in water
    
        if (pixel_x < BEACH_START_X and world[y][x] == 0 ):
            coin_type = random.choice(COIN_TYPES)
            coins[(x, y)] = coin_type

    return coins



def main():

    player_x = 5
    player_y = WORLD_HEIGHT // 2

    coins_type_0 = 0
    coins_type_1 = 0
    world = generate_world()
    coins = place_coins(world, 50)
    player_frame_index = 0
    animation_timer = 0
    animation_speed = 0.15
    cam_x = 0
    cam_y = 0

    direction = "right"

    running = True

    while running:

        dt = clock.tick(60) / 1000.0
        # --- Input ---

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_RIGHT]:
            dx = 1

        if keys[pygame.K_LEFT]:
            dx = -1

        if keys[pygame.K_DOWN]:
            dy = 1

        if keys[pygame.K_UP]:
            dy = -1

        nx = player_x + dx
        ny = player_y + dy

        moving = dx != 0 or dy != 0

        if moving:
            animation_timer += dt

            if animation_timer >= animation_speed:
                animation_timer = 0
                player_frame_index = (player_frame_index + 1) % len(player_frames)

        else:
            player_frame_index = 0
        if dx > 0:
            direction = "right"
        elif dx < 0:
            direction = "left"
        elif dy > 0:
            direction = "down"
        elif dy < 0:
            direction = "up"

        # Movement with boundaries and not on water

        if 0 <= nx < WORLD_WIDTH and 0 <= ny < WORLD_HEIGHT:
            pixel_x = nx * TILE_SIZE

            # Cannot enter beach
            if pixel_x < BEACH_START_X:

                # Cannot move through rocks
                if world[ny][nx] != 1:
                    player_x = nx
                    player_y = ny

        # Coin pickup

        if (player_x, player_y) in coins:
            coin_type = coins[(player_x, player_y)]
            if coin_type == 0:
                coins_type_0 += 1
            elif coin_type == 1:
                coins_type_1 += 1
            if coin_sound:
                coin_sound.play()
            del coins[(player_x, player_y)]

        # Camera centering

        cam_x = ( player_x * TILE_SIZE - SCREEN_WIDTH // 2+ TILE_SIZE // 2)
        cam_y = ( player_y * TILE_SIZE- SCREEN_HEIGHT // 2+ TILE_SIZE // 2)

        WORLD_PIXEL_WIDTH = WORLD_WIDTH * TILE_SIZE
        WORLD_PIXEL_HEIGHT = WORLD_HEIGHT * TILE_SIZE
        
        cam_x = max( 0,min( cam_x,WORLD_PIXEL_WIDTH - SCREEN_WIDTH))  
        cam_y = max( 0,min(cam_y,WORLD_PIXEL_HEIGHT - SCREEN_HEIGHT))
         # --- Draw ---

        screen.blit(water_bg, (-cam_x, -cam_y))
        screen.blit(beach_bg, (-cam_x, -cam_y))

        tile_x0 = max(0, cam_x // TILE_SIZE)
        tile_y0 = max(0, cam_y // TILE_SIZE)
        tile_x1 = min(WORLD_WIDTH,tile_x0 + SCREEN_WIDTH // TILE_SIZE + 2)
        tile_y1 = min(WORLD_HEIGHT,tile_y0 + SCREEN_HEIGHT // TILE_SIZE + 2 )

        for y in range(tile_y0, tile_y1):
            for x in range(tile_x0, tile_x1):
                tx = x * TILE_SIZE - cam_x
                ty = y * TILE_SIZE - cam_y

                t = world[y][x]

                if t == 1:
                    screen.blit(rock_img, (tx, ty))

        # Coin pickup
        
        for (x, y), coin_type in coins.items():

            tx = x * TILE_SIZE - cam_x
            ty = y * TILE_SIZE - cam_y

            if coin_type == 0:
                screen.blit(coin_img, (tx, ty))
            elif coin_type == 1:
                screen.blit(coin_img2, (tx, ty))

        # Player

        px = player_x * TILE_SIZE - cam_x
        py = player_y * TILE_SIZE - cam_y

        frame = player_frames[player_frame_index]

        if direction == "right":
            frame = pygame.transform.flip(frame, True, False)
        elif direction == "up":
            frame = pygame.transform.rotate(frame, -90)
        elif direction == "down":
            frame = pygame.transform.rotate(frame, 90)
        screen.blit(frame, (px, py))
        
        # HUD
        pygame.draw.rect(screen,HUD_BG,(0, 0, SCREEN_WIDTH, 30) )
        draw_text(screen,f"Sardines: {coins_type_0}",(10, 5),HUD_TEXT)
        draw_text(screen,f"Anchovies: {coins_type_1}",(220, 5),HUD_TEXT)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


# ======================================================
# START GAME
# ======================================================

if __name__ == "__main__":
    main()