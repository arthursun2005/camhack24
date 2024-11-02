from config import *

import pygame
from pygame.locals import *

import random
import player
from Spritesheet import Spritesheet
from scale import scale_image
import math


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

music = pygame.mixer.Sound("assets/music/m.wav")
music.play(-1)

def scale(arr, k):
    return [x * k for x in arr]

def get_input(pressed):
    dx, dy = 0, 0
    if pressed[K_RIGHT] or pressed[K_d]:
        dx += SPEED
    if pressed[K_LEFT] or pressed[K_a]:
        dx -= SPEED
    if pressed[K_UP] or pressed[K_w]:
        dy -= SPEED
    if pressed[K_DOWN] or pressed[K_s]:
        dy += SPEED
    mag = math.sqrt(dx * dx + dy * dy)
    if mag == 0:
        return dx, dy
    return dx / mag * SPEED, dy / mag * SPEED

def main():
    running = True
    tilesheet = Spritesheet('assets/texture/TX Tileset Grass.png', 16)
    camera_x = WORLD_WIDTH / 2
    camera_y = WORLD_HEIGHT / 2
    tiles = {}
    player1 = player.Player()
    for i in range(WORLD_HEIGHT):
        for j in range(WORLD_WIDTH):
            x = random.randint(0, tilesheet.w)
            y = random.randint(0, tilesheet.h)
            tile = scale_image(tilesheet.get_image(x, y), TILE_SIZE)
            tiles[i, j] = tile
    while running:
        keys = pygame.key.get_pressed()
        player1.move(keys)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        pressed = pygame.key.get_pressed()
        dx, dy = get_input(pressed)
        camera_x = min(WORLD_WIDTH - WIDTH - 1, max(0, camera_x + dx))
        camera_y = min(WORLD_HEIGHT - HEIGHT - 1, max(0, camera_y + dy))
        for x in range(int(camera_x), int(camera_x) + WIDTH + 1):
            for y in range(int(camera_y), int(camera_y) + HEIGHT + 1):
                pos_x = (x - camera_x) * TILE_SIZE
                pos_y = (y - camera_y) * TILE_SIZE
                screen.blit(tiles[y, x], tiles[y, x].get_rect(topleft=(pos_x, pos_y)))
        player1.update()
        screen.blit(player1.image,player1.rect)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
