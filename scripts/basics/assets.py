import pygame
import os

class Assets:
    def __init__(self, path):
        '''
        Initializes the Sprites class, setting up the directory for loading images.

        Parameters:
        - path: The base directory path where the 'images' folder is located.
        '''
        # Set the path to the 'images' directory by joining the base path with 'images'.
        self.images_dir = os.path.join(path, 'assets/images')
        self.audio_dir = os.path.join(path, 'assets/audio')
        self.ship_surf = pygame.image.load(os.path.join(self.images_dir, 'player.png')).convert_alpha()
        self.star_surf = pygame.image.load(os.path.join(self.images_dir, 'star.png')).convert_alpha()
        self.meteor_surf = pygame.image.load(os.path.join(self.images_dir, 'meteor.png')).convert_alpha()
        self.laser_surf = pygame.image.load(os.path.join(self.images_dir, 'laser.png')).convert_alpha()
        self.font_text = os.path.join(self.images_dir, 'Oxanium-Bold.ttf')
        self.explosion_surf = self.animated_sprites(pygame.image.load(os.path.join(self.images_dir, 'explosion.png')).convert_alpha(), 21, (5,5), (50,50))

        self.laser_sound = pygame.mixer.Sound(os.path.join(self.audio_dir, 'laser.wav'))
        self.explosion_sound = pygame.mixer.Sound(os.path.join(self.audio_dir, 'explosion.wav'))
        self.damage_sound = pygame.mixer.Sound(os.path.join(self.audio_dir, 'damage.ogg'))
        self.game_music = pygame.mixer.Sound(os.path.join(self.audio_dir, 'game_music.wav'))
    
    def groups(self):
        self.all_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.laser_sprites = pygame.sprite.Group()

    def animated_sprites(self, image, frames, matrix, image_size):
        images_frames = []
        count = 1
        for y in range (matrix[0]):
            for x in range(matrix[1]):
                if count <= frames:
                    images_frames.append(image.subsurface(pygame.Rect(x * image_size[0], y * image_size[1], image_size[0], image_size[1])))
                    count += 1
        return images_frames