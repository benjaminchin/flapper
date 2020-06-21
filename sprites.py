# Sprite classes for platform game
import pygame as pg
from settings import *
import random

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game, bird_sprites):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.bird_sprites = bird_sprites
        self.sprite_frame = 0
        self.image_orig = self.bird_sprites[self.sprite_frame]
        self.image = self.image_orig
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(15, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        #Rotation
        self.rot = 0 # rotation degree
        self.last_update = pg.time.get_ticks()

    def jump(self):
        if self.pos.y > 25:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        # self.rotate()
        self.animate()
        self.rotate()
        
        self.acc = vec(0, PLAYER_GRAV)
        """keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC"""

        self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        """if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH"""

        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)

    def rotate(self):
        """now = pg.time.get_ticks()
        
        self.last_update = now"""
        self.rot = (self.vel.y * -3)
        if self.rot < -90:
            self.rot = -90
            
        new_image = pg.transform.rotate(self.bird_sprites[self.sprite_frame], self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        # self.animate()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 100:
            self.last_update = now
            self.sprite_frame = (self.sprite_frame + 1)% 4
            self.image = self.bird_sprites[self.sprite_frame]
            

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.scored = False


class Spritesheet:
    # utility class for loading and parsing sprites
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab and image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 2, height * 2))
        image.set_colorkey(BLACK)
        return image
