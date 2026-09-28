# This file was created by: Logan Chavez
# Code inspired by game dev Chris Bradfield who was inspired by Notch

import pygame as pg
from os import path
from sprites import *
from settings import *
from utils import *

# Writing out some ideas
'''
Data types: boolean, JSON, strings, 
Input (events): Keyboard, Mouse, right click, voice, power button, 
eye tracking, camera, gyroscoping, electrostatic, location, volume

Process: cursor position, position of the player, score, enemy position, 
velocity, aim in FPS, 

Output: things are drawn, sounds: jump, power up, walking, haptics
'''


class Game:
    # initiate the game and characters
    def __init__ (self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("game initialized...")
        pg.display.set_caption(TITLE)
        self.running = True
        self.playing = True
        self.clock = pg.time.Clock()
    
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.image_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.map = Map(path.join(self.game_dir, map))
    # adds images, audio, and map
    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
  
        # self.wall = Wall(self, 10, 10)
        self.mob = Mob(self, 5, 0)
    # adds all sprites

        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "P":
                    Player(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
        # for row, tiles in enumerate(self.map.data):
        #             for col, tile, in enumerate(tiles):
        #                 if tile == "P":
        #                    Wall(self, col, row)
    # runs the game
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    # lets you close the tab when game ends
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
    # creates an output for the screen color
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
if __name__ == "__main__":
    g = Game()

    
# runs the game
while g.running:
    g.new()
    g.run()