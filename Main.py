import pygame
from sys import exit
from settings import *
from tiles import Tile
from level import Level
# from Bullet_Guns import *
# from player import player

#pygame setup
pygame.init()
pygame.display.set_caption("GunScape")
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
Level = Level(level_map, screen)
# gun = Gun(player.current_pos())

#Game running
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("blue")


    Level.run()

    pygame.display.update()
    clock.tick(60)



