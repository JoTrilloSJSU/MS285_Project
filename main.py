#Code has bee modified form below:
# Créé par Administrateur, le 23/05/2025 en Python 3.7
# https://github.com/Gruikjr/webol

import pygame
import random
import sys
import os

pygame.init()

#constants
TILE_SIZE = 64
WORLD_WIDTH = 31
WORLD_HEIGHT = 31
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BEACH_START_X = 1400

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
beach_bg = pygame.transform.scale( beach_bg,(WORLD_PIXEL_WIDTH, WORLD_PIXEL_HEIGHT))

# Obstacles and coins
rock_img = pygame.image.load("assets/sprites/rock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img,(TILE_SIZE, TILE_SIZE))
coin_img = pygame.image.load( "assets/sprites/fish.png").convert_alpha()
coin_img2 = pygame.image.load( "assets/sprites/fish2.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img,(TILE_SIZE +8, TILE_SIZE +8))
coin_img2 = pygame.transform.scale(coin_img2,(TILE_SIZE +8, TILE_SIZE+8))


# Player animation frames
player_frames = []

for i in range(4):
    img = pygame.image.load( f"assets/sprites/sealion-frames/pixil-frame-{i}.png").convert_alpha()
    img = pygame.transform.scale(img,(TILE_SIZE + 16, TILE_SIZE + 16))
    player_frames.append(img)

#sound
try:
    coin_sound = pygame.mixer.Sound(file=None)

except:
    coin_sound = None


def draw_text(surface, text, pos, color):
    img = font.render(text, True, color)
    surface.blit(img, pos)


def generate_world():  #note: used AI to help with this function
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


def place_coins(world, n, sst_condition):
    coins = {}

    while len(coins) < n:
        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)
        pixel_x = x * TILE_SIZE
        if pixel_x < BEACH_START_X and world[y][x] == 0:

            # cold fish distributions
            if sst_condition == "cold":
                if x < WORLD_WIDTH // 2:
                    coin_type = random.choices([0, 1], weights=[1, 4])[0]
                else:
                    coin_type = random.choices([0, 1],weights=[2, 1])[0]

           #warm fish distributions
            elif sst_condition == "warm":
                if x > WORLD_WIDTH // 2:
                    coin_type = random.choices([0, 1],weights=[5, 1])[0]
                else:
                    coin_type = random.choices( [0, 1], weights=[2, 2])[0]
            coins[(x, y)] = coin_type
    return coins



def sst_menu():

    selected_sst = "cold"

    while True:
        screen.fill((20, 40, 80))

        title = font.render( "Welcome to the Sea Lion Forager 2000!",True,(255,255,255))

        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        subtitle = font.render("Select Sea Surface Temperature Conditions",True,(255,255,255))

        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 170))
        screen.blit(subtitle, subtitle_rect)

        cold_color = (0, 200, 255) if selected_sst == "cold" else (180,180,180)
        warm_color = (255, 120, 80) if selected_sst == "warm" else (180,180,180)

        cold_text = font.render("COLD (Strong Upwelling)",True,cold_color)
        warm_text = font.render("WARM (El Niño Conditions)",True,warm_color)

        cold_rect = cold_text.get_rect(center=(SCREEN_WIDTH // 2, 240))
        warm_rect = warm_text.get_rect(center=(SCREEN_WIDTH // 2, 290))

        screen.blit(cold_text, cold_rect)
        screen.blit(warm_text, warm_rect)
        instructions = font.render("Eat 20 fish before your fat deposits run out!",True,(255,255,255))
        instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, 380))
        screen.blit(instructions, instructions_rect)
        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_sst = "cold"
                elif event.key == pygame.K_DOWN:
                    selected_sst = "warm"
                elif event.key == pygame.K_RETURN:
                    return selected_sst

def science_screen(sst_condition):

    waiting = True

    while waiting:

        screen.fill((15, 30, 60))

        if sst_condition == "cold":
            lines = [

                "Strong coastal upwelling brings cold,",
                "nutrient-rich water to the surface.",
                "Anchovies become more abundant nearshore.",
                "Try foraging close to the coast!"
            ]

        elif sst_condition == "warm":
            lines = [
                "El Niño conditions weaken upwelling",
                "and warm the California Current.",
                "Sardines shift farther offshore",
                "and anchovy abundance decreases.",
                "Try foraging offshore to eat energy dense sardines!"
            ]

        y = 140

        for line in lines:

            text = font.render(line, True, (255,255,255))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(text, rect)

            y += 35

        continue_text = font.render("Press ENTER to begin foraging :)",True,(255, 220, 120))
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, 430))
        screen.blit(continue_text, continue_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

def main():
    player_x = 5
    player_y = WORLD_HEIGHT // 2

    coins_type_0 = 0
    coins_type_1 = 0

    health = 100
    MAX_HEALTH = 100

    sst_condition = sst_menu()
    science_screen(sst_condition)
    world = generate_world()
    coins = place_coins(world, 50, sst_condition)

    player_frame_index = 0
    animation_timer = 0
    animation_speed = 0.15

    cam_x = 0
    cam_y = 0

    move_delay = 120
    last_move_time = 0
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

        current_time = pygame.time.get_ticks()

        if current_time - last_move_time > move_delay:

            nx = player_x + dx
            ny = player_y + dy

            last_move_time = current_time

        else:

            nx = player_x
            ny = player_y

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

            # Cannot go past beach
            beach_line = 20 + 0.015 * ny**2
            if nx < beach_line:

                # Cannot move through rocks
                if world[ny][nx] != 1:

                    # Only reduce health if player actually moves
                    if nx != player_x or ny != player_y:

                        player_x = nx
                        player_y = ny

                        health -= 2
                        health = max(0, health)

    

        # Coin pickup
        if (player_x, player_y) in coins:

            coin_type = coins[(player_x, player_y)]

            if coin_type == 0:
                coins_type_0 += 1 # Sardines are more enrgy efficient
                health += 10
                health = min(MAX_HEALTH, health)

            elif coin_type == 1:
                coins_type_1 += 1
                health += 5 #anchovies are less energy efficient
                health = min(MAX_HEALTH, health)

            if coin_sound:
                coin_sound.play()

            del coins[(player_x, player_y)]

            # if coins_type_0 >= 5 and coins_type_1 >= 5:
            #     running = False
        if coins_type_0 + coins_type_1 >= 20:
            running = False
        
        if health <= 0:
            running = False

        # Camera centering
        cam_x = (player_x * TILE_SIZE - SCREEN_WIDTH // 2+ TILE_SIZE // 2)
        cam_y = (player_y * TILE_SIZE- SCREEN_HEIGHT // 2+ TILE_SIZE // 2)

        WORLD_PIXEL_WIDTH = WORLD_WIDTH * TILE_SIZE
        WORLD_PIXEL_HEIGHT = WORLD_HEIGHT * TILE_SIZE

        cam_x = max( 0,min(cam_x, WORLD_PIXEL_WIDTH - SCREEN_WIDTH))
        cam_y = max( 0,min(cam_y, WORLD_PIXEL_HEIGHT - SCREEN_HEIGHT))

        # --- Draw ---
        screen.blit(water_bg, (-cam_x, -cam_y))
        screen.blit(beach_bg, (-cam_x, -cam_y))

        tile_x0 = max(0, cam_x // TILE_SIZE)
        tile_y0 = max(0, cam_y // TILE_SIZE)

        tile_x1 = min(WORLD_WIDTH,tile_x0 + SCREEN_WIDTH // TILE_SIZE + 2)
        tile_y1 = min(WORLD_HEIGHT,tile_y0 + SCREEN_HEIGHT // TILE_SIZE + 2)

        screen.blit(water_bg, (-cam_x, -cam_y))
        screen.blit(beach_bg, (-cam_x, -cam_y))

        for y in range(tile_y0,tile_y1):

            for x in range(tile_x0, tile_x1):

                tx = x * TILE_SIZE - cam_x
                ty = y * TILE_SIZE- cam_y

                t =  world[y][x]

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
        pygame.draw.rect(screen,HUD_BG,(0, 0, SCREEN_WIDTH, 60))
        draw_text(screen,f"Sardines: {coins_type_0}",(10, 5),HUD_TEXT)
        draw_text(screen,f"Anchovies: {coins_type_1}",(220, 5),HUD_TEXT)
        draw_text(screen, f"SST: {sst_condition.upper()}", (10, 35), HUD_TEXT)

        # Health bar
        pygame.draw.rect(screen,(100, 0, 0),(450, 5, 150, 20))

        pygame.draw.rect(screen,(0, 200, 0),(450,5,int(150 * (health / MAX_HEALTH)),20))
        draw_text(screen,"Fat Deposits",(380, 5),HUD_TEXT)
        pygame.display.flip()

    screen.fill((0, 0, 0))

    if health <= 0:
        msg = "Game Over!"

    else:
        msg = "You Win!"

    text = font.render(msg,True,(255, 255, 255))
    screen.blit(text,(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# START GAME

if __name__ == "__main__":
    main()