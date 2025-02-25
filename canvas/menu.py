import pygame
from scripts.basics.gui import Label, Button, Slider, TextBox

class Menu():
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
        # Setup a new menu screen.
        self.new_screen()
    
    def new_screen(self):
        '''
        Creates a new surface for the menu and initializes menu components.
        '''
        # Create a menu surface with the same size as the game screen.
        self.menu_screen = pygame.Surface((self.screen.WIDTH, self.screen.HEIGHT))

        # Create text and button elements for the menu.
        self.text = Label(self.menu_screen)
        self.button1 = Button(self.menu_screen, self.screen.aspect_ratio, (150, 150))
        self.button2 = Button(self.menu_screen, self.screen.aspect_ratio, (150, 300), border_radius=20, text_color=(0,0,255), text_hover_color=(255,0,0))
        self.button3 = Button(self.menu_screen, self.screen.aspect_ratio, (150, 450), shadow_size=(6,6))
        self.button4 = Button(self.menu_screen, self.screen.aspect_ratio, (500, 600), border=2, transparency=-1, text_hover_color=(128,128,128))
        self.button5 = Button(self.menu_screen, self.screen.aspect_ratio, (500, 150), border=2, border_radius=20)
        self.button6 = Button(self.menu_screen, self.screen.aspect_ratio, (500, 300), border_radius=20, shadow_size=(6,6), border=2)
        self.button7 = Button(self.menu_screen, self.screen.aspect_ratio, (500, 450), border_radius=20, shadow_size=(6,6), text_color=(255,255,255), text_hover_color=(255,255,255), button_color=(20,20,20), button_hover_color=(0,0,0), shadow_color=(100,100,100))
        self.button8 = Button(self.menu_screen, self.screen.aspect_ratio, (1200, 30), size=(150, 50), text_font_size=50, border_radius=20, shadow_size=(6,6), border=2)
        self.slider = Slider(self.menu_screen, self.screen.aspect_ratio, (850, 175), slider_value=self.settings.audio_settings['main_volume'])
        self.text_box = TextBox(self.menu_screen, self.screen.aspect_ratio, (500, 680), size=(500, 50), border=2, transparency=-1, border_radius=20)

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
        pass

    def events(self):
        '''
        Handle pygame events, including quitting the game.
        '''
        for event in pygame.event.get():
            # Quit the game if the window is closed.
            if event.type == pygame.QUIT:
                self.game.running = False
            self.text_box.event(event)
        
    def draw(self):
        self.text_box.draw()
        '''
        Draw the menu on the screen.
        '''
        # Scale the menu surface to fit the display surface.
        self.screen.scale_screen(self.menu_screen)
        # Fill the menu background with white.
        self.menu_screen.fill((255,255,255))

        # Draw buttons with corresponding text.
        self.button1.draw('1600x900')
        self.button2.draw('1280x720')
        self.button3.draw('720x480')

        # Display FPS status if enabled.
        if self.settings.video_settings['show_fps']:
            status = 'ON'
            self.text.write('FPS: ', (0, 550))
            self.text.write(str(int(self.screen.clock.get_fps())), (170, 550))
        else:
            status = 'OFF'
        self.button4.draw(f'{self.settings.game_texts['show_fps']} - {status}')

        # English language button.
        self.button5.draw('English')
        # Portuguese language button.
        self.button6.draw('Português')

        # Display VSync status.
        if self.settings.video_settings['vsync'] == 1:
            status = 'ON'
        else:
            status = 'OFF'
        self.button7.draw(f'VSync - {status}')

        # Draw the title text at the top-center of the screen.
        self.text.write(self.settings.game_texts['title'], (int(self.screen.WIDTH/2), 0), center_w=True)

        # Exit button.
        self.button8.draw(self.settings.game_texts['exit'])
        # Draw volume slider.
        self.slider.draw_slider()
        # Display current volume.
        self.text.write(self.settings.audio_settings['main_volume'], (850, 100), center_w=True)

    def inputs(self):
        '''
        Handle inputs, such as button clicks and slider interactions.
        '''
        # Handle resolution buttons.
        if self.button1.click():
            self.screen.resize_screen(1600, 900, self.settings.video_settings['vsync'])
            self.new_screen()
        if self.button2.click():
            self.screen.resize_screen(1280, 720, self.settings.video_settings['vsync'])
            self.new_screen()
        if self.button3.click():
            self.screen.resize_screen(720, 480, self.settings.video_settings['vsync'])
            self.new_screen()
        
        # Handle FPS toggle button.
        if self.button4.click():
            self.settings.set_settings('video', 'show_fps', False) if self.settings.video_settings['show_fps'] else self.settings.set_settings('video', 'show_fps', True)
        
        # Handle language buttons.
        if self.button5.click():
            self.settings.set_settings('language', 'language_set', 'en-US')
        if self.button6.click():
            self.settings.set_settings('language', 'language_set', 'pt-BR')
        
        # Handle VSync toggle button.
        if self.button7.click():
            self.settings.set_settings('video', 'vsync', 0) if self.settings.video_settings['vsync'] == 1 else self.settings.set_settings('video', 'vsync', 1)
            self.screen.resize_screen(self.settings.video_settings['width'], self.settings.video_settings['height'], self.settings.video_settings['vsync'])
        
        # Handle exit button.
        if self.button8.click():
            self.game.running = False
        
        # Handle slider interaction.
        if self.slider.click_slider():
            self.settings.set_settings('audio', 'main_volume', self.slider.slider_value)
        
        # Handle text_box interaction.
        self.text_box.click()
