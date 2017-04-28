# setting
import random
title = 'Mangster Jump'

width = 480
height = 650
fps = 60

font_name = 'Bauhaus 93'
hs_file = 'highscore.txt'

ai_freq = random.randrange(7000,20000)

player_layer = 3
platform_layer = 0
pow_layer = 2
mob_layer = 2
coin_layer = 2

player_acc = 0.75
player_friction = 0.003
# start platform
platform_list = [(0,height -60),
                 ((width/2, height -30)),
                 (width/2, height - 150),
                 (125, height - 350),
                 (350,200),(175,100,)]
player_jump = 16

# define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)

spritesheet = 'spritesheet_jumper.png'


#boot
boost_power = 30
pow_spaw = 5

#bur
bur_spaw = 4
#coin
coin_spaw = 3