import pygame
import random

class Meteor(pygame.sprite.Sprite):
    def __init__(self, game, image, groups):
        super().__init__(groups)
        self.game = game
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_frect(midbottom=(random.randint(0, self.game.screen.WIDTH), 0))
        self.speed = random.randint(50, 300)
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.creation_time = pygame.time.get_ticks()
        self.rotation = 0
        self.rotation_speed = random.randint(-100, -50) if random.randint(0,1) == 0 else random.randint(50, 100)
    
    def update(self, delta_time):
        self.direction.normalize()
        self.rect.center += self.speed * self.direction * delta_time
        if self.rect.top >= self.game.screen.HEIGHT:
            self.kill()
        self.rotation += self.rotation_speed * delta_time
        self.image = pygame.transform.rotozoom(self.original_image, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
