import pygame

class Tile(pygame.sprite.Sprite): #pygame.sprite.Sprite helps you by giving some shortcuts and grouping
    def __init__(self,pos,size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift #this will move the cube in x position