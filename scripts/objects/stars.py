import pygame
from random import randint

class Stars(pygame.sprite.Sprite):
    def __init__(self, game, image, groups):
        super().__init__(groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_frect(center = (randint(0, self.game.screen.WIDTH), randint(0, self.game.screen.HEIGHT)))
    
    def update(self, delta_time):
        pass
    