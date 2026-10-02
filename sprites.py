# imports pygame
import pygame as pg
# allows us to access settings
from settings import *
# imports sprites
from pygame.sprite import Sprite
from utils import *

from os import path

vec = pg.math.Vector2

# It tells you when two objects collide
def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    # check for x collision
    if dir == 'x':
        # checking if we collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # this line checks to see if we're to the left of the wall
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                # reposition the player (sprite) to the left side of the wall
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.height / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                # reposition the player (sprite) to the right side of the wall
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.height / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
         # checking if we collided with hitrects
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # this line checks to see if we're to the left of the wall
            if hits[0].rect.centery > sprite.hit_rect.centery:
                # reposition the player (sprite) to the left side of the wall
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.width / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                # reposition the player (sprite) to the right side of the wall
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.width / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
        

# adds a new class
class Player(Sprite):
    def __init__(self, game, x, y):
        # puts the player into all_sprites group
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # makes the player the avatar from spritesheet
        self.spritesheet = Spritesheet(path.join(self.game.image_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE, TILESIZE)
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        # makes the velocity zero when you collide
        self.vel = vec(0,0)
        self.pos = vec(x*TILESIZE,y*TILESIZE)
        self.last_update = 0
        self.current_frame = 0
        # self.vx, self.vy = 0,0
        # self.x = x*TILESIZE
        # self.y = y*TILESIZE
        # print("player initialized")
        # print(self.rect.x)
        # print(self.rect.y)

    def get_keys(self):
        # reset v to zero
        # listen for events specific to keys
        # change velocity based on which key is pressed
        self.vel = vec(0,0)
        keys = pg.key.get_pressed()
        # makes the player move through user input
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            # self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
                    self.vel.x = PLAYER_SPEED
                    # self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
                    self.vel.y = -PLAYER_SPEED
                    # self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
                    self.vel.y = PLAYER_SPEED
                    # self.vy = PLAYER_SPEED
                # check to see if player si moving diagonal
        # makes you move diagonal the same speed
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    def animate(self):
        # use the time element to get now
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            bottom = self.rect.bottom
            self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    # animates the player
    def load_images(self):
        self.idle_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]
        self.jump_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE),
                            self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)
                            ]

    # makes it so the player keeps updating
    def update(self):
        self.get_keys()
        self.animate()
        # makes the collision with walls work
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center

            

       

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # makes the walls red
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        # print("wall initialized")
        # print(self.rect.x)
        # print(self.rect.y)

    def update(self):
        pass
        # wallhits = pg.sprite.spritecollide(self, self.game.all_walls, True)
        # if wallhits:
        #     wallhits[0].kill()

class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # makes the mobs blue
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        # sets speed
        self.speed = 20
        self.vx, self.vy = 5,0
        self.x = x*TILESIZE
        self.y = y*TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        print("mob initialized")
        print(self.rect.x)
        print(self.rect.y)

    def update(self):
        # thanks pygame
        if self.rect.right > WIDTH or self.rect.left < 0:
              self.speed *= -1
              self.y += TILESIZE
        
            
        # sets the speed
        self.x += self.vx * self.game.dt * self.speed
        self.rect.x = self.x
        self.y += self.vy * self.game.dt * self.speed
        self.rect.y = self.y


        
