import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, game, image, groups):
        super().__init__(groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_frect(center = (self.game.screen.WIDTH/2, self.game.screen.HEIGHT/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        self.shoot = True
        self.shoot_time = 0
        self.shoot_duration = 400
        self.meteors_destroyed = 0
    
    def shoot_timer(self):
        if not self.shoot:
            current_time = pygame.time.get_ticks()
            if (current_time - self.shoot_time) >= self.shoot_duration:
                self.shoot = True
    
    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.key.key_code(self.game.settings.controls['right'])]) - int(keys[pygame.key.key_code(self.game.settings.controls['left'])])
        self.direction.y = int(keys[pygame.key.key_code(self.game.settings.controls['down'])]) - int(keys[pygame.key.key_code(self.game.settings.controls['up'])])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time
        
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.game.screen.HEIGHT:
            self.rect.bottom = self.game.screen.HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.game.screen.WIDTH:
            self.rect.right = self.game.screen.WIDTH
        
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.key.key_code(self.game.settings.controls['shoot'])] and self.shoot:
            Laser(self.game, self.game.assets.laser_surf, (self.game.assets.all_sprites, self.game.assets.laser_sprites), self.rect.midtop)
            self.game.assets.laser_sound.play()
            self.shoot_time = pygame.time.get_ticks()
            self.shoot = False
        
        self.shoot_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, game, image, groups, ship_pos):
        super().__init__(groups)
        self.game = game
        self.image = image
        self.rect = self.image.get_frect(midbottom = (ship_pos[0], ship_pos[1]))
        self.speed = 500
    
    def update(self, delta_time):
        self.rect.y -= self.speed * delta_time
        
        if self.rect.bottom <= 0:
            self.kill()
        
        if pygame.sprite.groupcollide(self.game.assets.laser_sprites, self.game.assets.meteor_sprites, True, True, pygame.sprite.collide_mask):
            Explosion(self.game, self.game.assets.explosion_surf, self.game.assets.all_sprites, self.rect.midtop)
            self.game.assets.explosion_sound.play()
            self.game.ship.meteors_destroyed += 1

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, image, groups, pos):
        super().__init__(groups)
        self.game = game
        self.frames = image
        self.image = self.frames[0]
        self.rect = self.image.get_frect(center=pos)
        self.frames_speed = 50
        self.frame_index = 0
    
    def update(self, delta_time):
        self.frame_index += self.frames_speed * delta_time
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        if len(self.frames) == int(self.frame_index) % len(self.frames) + 1: 
            self.kill()
