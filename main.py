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

GOALS: make money, own cars, commit crimes

RULES: can't fly, can't shoot through walls, can't leave map

FEEDBACK: when taking damage screen turns red, recoil, money counter

FREEDOM: walks wherever
'''



class Game:
    # initiate the game and characters
    def __init__ (self):
        pg.init()
        pg.mixer.init()
        # creates a screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("game initialized...")
        pg.display.set_caption(TITLE)
        # sets it so that we are running the game
        self.running = True
        self.playing = True
        # adds a clock
        self.clock = pg.time.Clock()
        # adds a high score
        self.high_score = 0
        self.score = 0
    # adds images, audio, and map
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.game_save_file = path.join(self.game_dir, "highscore.txt")
        self.image_dir = path.join(self.game_dir, 'images')
        # sound handling
        self.snd_dir = path.join(self.game_dir, 'audio')
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "bell.wav"))
        self.map = Map(path.join(self.game_dir, map))

        try:
            with open(self.game_save_file, 'x', encoding="utf-8") as file:
                file.write("hello world!")
            print("file created successfully!")
        except FileExistsError:
            print("File already exists")

        with open(self.game_save_file, 'r') as file:
            try:
                self.high_score = int(file.read())
            except:
                self.high_score = 0
                print("high score set to zero")    
    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_particles = pg.sprite.Group()
  
        # self.wall = Wall(self, 10, 10)
        self.mob = Mob(self, 5, 0)
        

        # adds all sprites into the game
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                if tile == "C":
                    Coin(self, col, row)
                if tile == "M":
                    Mob(self, col, row)
        for row, tiles in enumerate(self.map.data):
                    for col, tile, in enumerate(tiles):
                        if tile == "P":
                           self.player = Player(self, col, row)
        pg.mixer.music.load(path.join(self.snd_dir, "one_0.mp3"))
        pg.mixer.music.play(loops=-1)
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
            # joins and reads the highscore file
            if event.type == pg.QUIT:
                # keeps the highest score
                if self.score > self.high_score:
                    with open(path.join(self.game_dir, self.game_save_file), 'w') as file:
                        file.write(str(self.score))
                if self.playing:
                    self.playing = False
                self.running = False
    # adds text
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)
    # updates all the sprites
    def update(self):
        self.all_sprites.update()
    
    # creates an output for the screen color
    def draw(self):
        # order matters because the first things are on the bottom because they are the 'first' to be drawn
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # adds the text to screen
        self.draw_text("Frames per second: " + str(floor(1/self.dt) ), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Coins: " + str(floor(self.player.coins) ), 24, WHITE, WIDTH/2, HEIGHT/7)
        self.draw_text("Score: " + str(floor(self.score) ), 24, WHITE, WIDTH/2, HEIGHT/5)
        self.draw_text("High Score: " + str(floor(self.high_score) ), 24, WHITE, WIDTH/2, HEIGHT/8)
        pg.display.flip()

# if the file is named main you run the game
if __name__ == "__main__":
    g = Game()

    
# runs the game
while g.running:
    g.new()
    g.run()