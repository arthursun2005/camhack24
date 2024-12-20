from config import *
from utils import *

from collections import deque
from dialogue import Dialogue

from Spritesheet import Spritesheet
from animation import Animation

import pygame
from pygame.math import Vector2
from pygame.math import clamp
import random

NPC_CLEAR_QUEUE = 1

class NPC(pygame.sprite.Sprite):
    def __init__(self, id, x, y):
        super().__init__()
        self.id = id

        self.sus = 0
        self.actions = deque()
        self.dialogue = None
        self.killed = False
        self.health = NPC_HEALTH
        self.dmg = NPC_DMG
        self.speed = NPC_SPEED / TILE_SIZE

        spritesheet = Spritesheet("assets/Cute_Fantasy_Free/Enemies/Skeleton.png", 32)

        self.down = (Animation(spritesheet, 5, [18, 19, 20, 21, 22, 23]), Animation(spritesheet, 5, [0]), Animation(spritesheet, 5, [36, 37, 38, 39]))
        self.right = (Animation(spritesheet, 5, [24, 25, 26, 27, 28, 29]), Animation(spritesheet, 5, [6]), Animation(spritesheet, 5, [42, 43, 44, 45]))
        self.up = (Animation(spritesheet, 5, [30, 31, 32, 33, 34, 35]), Animation(spritesheet, 5, [12]), Animation(spritesheet, 5, [48, 49, 50, 51]))

        self.killanim = Animation(spritesheet, 20, [36, 37, 38] + [39] * 8000)

        self.real_pos = Vector2(x, y)
        self.pos = Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        self.size = PLAYER_SIZE

        self.image = scale_image(spritesheet.get_image(0, 0), self.size)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))

        self.target = Vector2(random.randint(0, WORLD_WIDTH), random.randint(0, WORLD_HEIGHT))
        self.good_target = False

        self.run = False
        self.orit = 0

        self.friend = 50

    def queue_action(self, action, flags):
        if flags and NPC_CLEAR_QUEUE:
            self.actions.clear()
        self.actions.append(action)

    def random_target(self):
        return Vector2(random.randint(0, WORLD_WIDTH - 1), random.randint(0, WORLD_HEIGHT - 1))
    
    def set_run(self):
        self.run = True
        self.speed = NPC_RUN_SPEED / TILE_SIZE
    
    def reset_run(self):
        self.run = False
        self.speed = NPC_SPEED / TILE_SIZE

    def update(self, player_pos):
        self.health = max(0, self.health)
        if self.health <= 0:
            self.killed = True
        
        if self.killed:
            img = self.killanim.get_image(0)
            self.image = scale_image(img, self.size)
            self.rect = self.image.get_rect(center=self.pos)
            return
        
        if self.real_pos == self.target or not self.good_target:
            if random.random() < RANDOM_CHANCE:
                self.target = self.random_target()
        
        if self.real_pos == self.target:
            self.good_target = False

        direction = self.target - self.real_pos
        if self.run:
            direction = -(player_pos - self.real_pos)
            if random.random() < RANDOM_WALK_CHANCE:
                self.run = False
                self.speed = NPC_SPEED / TILE_SIZE
                self.target = self.random_target()
        
        self.real_pos += direction.normalize() * self.speed
        self.real_pos.x = clamp(self.real_pos.x, 0, WORLD_WIDTH)
        self.real_pos.y = clamp(self.real_pos.y, 0, WORLD_HEIGHT)

        self.orit = get_orient(direction)
        ii = 0
        if self.orit == RIGHT:
            img = self.right[ii].get_image(0)
        if self.orit == UP:
            img = self.up[ii].get_image(0)
        if self.orit == LEFT:
            img = self.right[ii].get_image(0)
            img = pygame.transform.flip(img, 1, 0)
        if self.orit == DOWN:
            img = self.down[ii].get_image(0)
        self.image = img
