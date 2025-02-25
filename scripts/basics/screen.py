import pygame

class Screen():
    '''
    Manages the game screen, including resolution, scaling, and frame timing.
    '''
    def __init__(self, settings):
        '''
        Initializes the Screen class.

        Parameters:
        - settings: An instance of the Settings class, used to configure screen settings.

        Attributes:
        - WIDTH: Default screen width (used as a reference for scaling);
        - HEIGHT: Default screen height (used as a reference for scaling);
        - display_surf: The main display surface for rendering;
        - clock: A Pygame clock object for managing frame timing.
        '''
        self.settings = settings
        # Default reference dimensions for screen scaling.
        self.WIDTH = 1280
        self.HEIGHT = 720
        # Set up the screen using settings from the Settings instance.
        self.set_screen(self.settings.video_settings['width'], self.settings.video_settings['height'], self.settings.video_settings['vsync'])
        # Clock to manage frame timing.
        self.clock = pygame.time.Clock()

    def set_screen(self, width, height, vsync):
        '''
        Sets up the screen with the given width, height, and vsync settings.

        Parameters:
        - width: The desired screen width;
        - height: The desired screen height;
        - vsync: A boolean indicating whether vsync is enabled.

        Sets:
        - display_surf: The main Pygame display surface;
        - width_ratio: The ratio between the current width and the default width;
        - height_ratio: The ratio between the current height and the default height;
        - aspect_ratio: A tuple containing the width and height scaling ratios.
        '''
        self.display_surf = pygame.display.set_mode((width, height), vsync=vsync)
        # Calculate scaling ratios based on the default dimensions.
        self.width_ratio = width / self.WIDTH
        self.height_ratio = height / self.HEIGHT
        self.aspect_ratio = (self.width_ratio, self.height_ratio)
        # Set the window title.
        pygame.display.set_caption(self.settings.game_texts['title'])
        
    
    def scale_screen(self, screen):
        '''
        Scales the provided surface to fit the display surface.

        Parameters:
        - screen: The surface to scale.
        '''
        pygame.transform.smoothscale(screen, self.display_surf.get_size(), self.display_surf)
    
    def resize_screen(self, width, height, vsync):
        '''
        Resizes the game screen and updates the video settings.

        Parameters:
        - width: The new screen width;
        - height: The new screen height;
        - vsync: A boolean indicating whether vsync is enabled.

        Steps:
        - Updates the video settings in the Settings instance;
        - Quits the current display and sets up a new one with the updated settings.
        '''
        # Update the video settings stored in the Settings object.
        self.settings.set_settings('video', 'width', width)
        self.settings.set_settings('video', 'height', height)
        self.settings.set_settings('video', 'vsync', vsync)
        # Restart the display to apply the new settings.
        pygame.display.quit()
        pygame.mixer.quit()
        self.set_screen(width, height, vsync)
    
    def delta_time(self):
        '''
        Calculates the time since the last frame.

        Sets:
        - dt: Delta time in seconds, based on the desired frames per second (fps) from the settings.
        '''
        self.dt = self.clock.tick(self.settings.video_settings['fps']) / 1000
    
    def screen_update(self):
        '''
        Updates the entire display window, rendering any changes.
        '''
        pygame.display.update()
