import pygame
from scripts.basics.assets import Assets
from scripts.objects.stars import Stars
from scripts.objects.ship import Ship
from scripts.objects.meteor import Meteor
from scripts.basics.gui import Label

class SpaceShooter():
    '''
    Handles the game menu, including buttons, sliders, and user interactions.
    '''
    def __init__(self, game):
        '''
        Initializes the menu, creating a new screen and menu elements.
        '''
        # Reference to the main game instance.
        self.game = game
        # Access game settings.
        self.settings = game.settings
        # Access the game's screen.
        self.screen = game.screen
        self.assets = Assets(self.settings.path)
        # Setup a new menu screen.
        self.new_screen()
    
    def new_screen(self):
        '''
        Creates a new surface for the menu and initializes menu components.
        '''
        # Create a menu surface with the same size as the game screen.
        self.assets.groups()
        self.canvas_surf = pygame.Surface((self.screen.WIDTH, self.screen.HEIGHT))
        for _ in range (20):
            Stars(self, self.assets.star_surf, self.assets.all_sprites) 
        self.ship = Ship(self, self.assets.ship_surf, self.assets.all_sprites)
        self.meteor_event = pygame.event.custom_type()
        self.score_text = Label(self.canvas_surf, (255, 255, 255), font=self.assets.font_text, border_color=(255,255,255), border_radius=10, font_size=80, border_padding=15, border_width=5)
        pygame.time.set_timer(self.meteor_event, 500)
        self.assets.game_music.play(loops=-1)

    def run(self):
        '''
        Main loop to handle menu logic.
        '''
        # Process events.
        self.events()
        # Update logic (if any).
        self.update()
        # Render menu elements.
        self.draw()
        # Handle user interactions.
        self.inputs()
    
    def update(self):
        '''
        Update menu components (currently unused).
        '''
        self.assets.all_sprites.update(self.screen.dt)
        if pygame.sprite.spritecollide(self.ship, self.assets.meteor_sprites, True, pygame.sprite.collide_mask):
            self.assets.damage_sound.play()

    def events(self):
        '''
        Handle pygame events, including quitting the game.
        '''
        for event in pygame.event.get():
            # Quit the game if the window is closed.
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == self.meteor_event:
                Meteor(self, self.assets.meteor_surf, (self.assets.all_sprites, self.assets.meteor_sprites))
        
    def draw(self):
        '''
        Draw the menu on the screen.
        '''
        # Scale the menu surface to fit the display surface.
        self.screen.scale_screen(self.canvas_surf)
        # Fill the menu background with white.
        self.canvas_surf.fill((58,46,63))
        self.assets.all_sprites.draw(self.canvas_surf)
        self.score_text.write(self.ship.meteors_destroyed, (self.game.screen.WIDTH/2, self.game.screen.HEIGHT-100), True)

    def inputs(self):
        '''
        Handle inputs, such as button clicks and slider interactions.
        '''
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_0]:
            self.screen.resize_screen(720, 480, 0)
            self.new_screen()
        if recent_keys[pygame.K_1]:
            self.screen.resize_screen(1280, 720, 0)
            self.new_screen()
