import pygame
import time

class Text():
    def __init__(self, screen, text_color, text_antialias, font, font_size):
        '''
        Initializes a Text object for rendering text on the screen.

        Parameters:
        - screen: The Pygame screen where the text will be rendered;
        - text_color: Color of the text (RGB tuple);
        - text_antialias: Boolean to enable or disable antialiasing;
        - font: Path to the font file or None for the default font;
        - font_size: Size of the font.
        '''
        # Create a font object with the specified font and size.
        self.text_font = pygame.font.Font(font, font_size)
        # Store screen, text color, and antialiasing properties.
        self.screen = screen
        self.text_color = text_color
        self.text_antialias = text_antialias

class Label(Text):
    def __init__(self, screen, text_color=(0,0,0), text_antialias=True, font=None, font_size=100, border_radius=0, border_color=(0,0,0), border_width=2, border_padding=0):
        '''
        Initializes a Label object, inheriting from Text.

        Parameters:
        - screen: The Pygame screen where the label will be rendered;
        - text_color: Color of the text (default is black);
        - text_antialias: Boolean to enable or disable antialiasing (default is True);
        - font: Path to the font file or None for the default font;
        - font_size: Size of the font (default is 100).
        '''
        super().__init__(screen, text_color, text_antialias, font, font_size)
        self.border_radius = border_radius
        self.border_color = border_color
        self.border_width = border_width
        self.border_padding = border_padding
    
    def write(self, text, pos, center_w=False, center_h=False):
        '''
        Renders and draws text on the screen.

        Parameters:
        - text: The string to be displayed;
        - pos: Tuple (x, y) indicating the position on the screen;
        - center_w: Boolean to center the text horizontally around pos[0];
        - center_h: Boolean to center the text vertically around pos[1].
        '''
        # Render the text as a surface with the specified font, color, and antialiasing.
        text_surf = self.text_font.render(str(text), self.text_antialias, self.text_color)
        # Calculate offsets for centering the text, if enabled.
        center_width = text_surf.get_width() / 2 if center_w else 0
        center_height = text_surf.get_height() / 2 if center_h else 0
        text_rect = text_surf.get_frect(topleft=(pos[0] - center_width, pos[1] - center_height))
        # Blit the text surface onto the screen at the adjusted position.
        self.screen.blit(text_surf, (pos[0] - center_width, pos[1] - center_height))
        pygame.draw.rect(self.screen, self.border_color, text_rect.inflate(self.border_padding, -self.border_padding).move(0, -self.border_padding/1.5), self.border_width, self.border_radius)

class TextButton(Text):
    def __init__(self, screen, text_color, text_antialias, font, font_size):
        '''
        Initializes a TextButton object, inheriting from Text.

        Parameters:
        - screen: The Pygame screen where the button text will be rendered;
        - text_color: Color of the text;
        - text_antialias: Boolean to enable or disable antialiasing;
        - font: Path to the font file or None for the default font;
        - font_size: Size of the font.
        '''
        super().__init__(screen, text_color, text_antialias, font, font_size)
    
    def write(self, text, pos, buttom_width, center=True):
        '''
        Renders and draws text on the screen, optionally resizing it to fit within a button.

        Parameters:
        - text: The string to be displayed;
        - pos: Tuple (x, y) indicating the position on the screen;
        - buttom_width: The maximum width allowed for the text (0 for no limit);
        - center: Boolean to center the text both horizontally and vertically around pos;
        '''
        # Render the text as a surface.
        text_surf = self.text_font.render(text, self.text_antialias, self.text_color)
        # If the button's width is smaller than the text's width, scale the text down.
        if buttom_width < text_surf.get_width() and buttom_width != 0:
            # Scale the text surface to fit within the button width (subtracting 20 for padding).
            text_surf = pygame.transform.scale_by(text_surf, (buttom_width-20) / text_surf.get_width())
        # Calculate offsets for centering the text, if enabled.
        center_width = text_surf.get_width() / 2 if center else 0
        center_height = text_surf.get_height() / 2 if center else 0
        # Blit the text surface onto the screen at the adjusted position.
        self.screen.blit(text_surf, (pos[0] - center_width, pos[1] - center_height))

class TextBoxContent(Text):
    def __init__(self, screen, text_color, text_antialias, font, font_size):
        super().__init__(screen, text_color, text_antialias, font, font_size)
        self.text_surf = self.text_font.render('', self.text_antialias, self.text_color)
    
    def write(self, text, pos, offset, text_box_size, padding, center_h=True):
        self.text_surf = self.text_font.render(text, self.text_antialias, self.text_color)
        center_height = text_box_size[1]/3 if center_h else 0
        clip_surface = pygame.Surface(((text_box_size[0]-(padding*2)), text_box_size[1]), pygame.SRCALPHA)
        clip_surface.fill((0,0,0,0))
        clip_surface.blit(self.text_surf, (-offset, 0))
        self.screen.blit(clip_surface, ((pos[0]+padding), pos[1]+center_height))

### REVIEW ###
class Button(TextButton):
    def __init__(self, screen, aspect_ratio, pos, size=(300, 100), text_color=(0,0,0), text_hover_color=(0,0,0), visible=True, text_antialias=True, text_font=None, text_font_size=100, button_color=(128,128,128), button_hover_color=(100,100,100), shadow_size=(0,0), shadow_color=(0,0,0), border=-1, border_color=(0,0,0), border_radius=0, transparency=0):
        '''
        Initializes the Button object, which inherits from the TextButton class.

        Parameters:
        - screen: The Pygame screen to draw the button on;
        - pos: Tuple containing the x and y position of the button;
        - size: Size of the button as a tuple (width, height). Default is (300, 100);
        - text_color: Color of the text on the button. Default is black (0, 0, 0);
        - text_hover_color: Color of the text when the button is hovered. Default is black (0, 0, 0);
        - text_antialias: Whether to enable antialiasing for text. Default is True;
        - text_font: Font used for the text. Default is None;
        - text_font_size: Size of the text font. Default is 100;
        - button_color: Default color of the button. Default is gray (128, 128, 128);
        - button_hover_color: Color of the button when hovered. Default is gray (100, 100, 100);
        - shadow_size: Size of the shadow as a tuple (x_offset, y_offset). Default is (0, 0);
        - shadow_color: Color of the shadow. Default is black (0, 0, 0);
        - border: Border thickness. Default is -1 (no border);
        - border_color: Color of the border. Default is black (0, 0, 0);
        - border_radius: Radius for rounded button corners. Default is 0;
        - transparency: Transparency level. Default is 0 (fully opaque).
        '''
        super().__init__(screen, text_color, text_antialias, text_font, text_font_size)
        self.screen = screen
        self.aspect_ratio = aspect_ratio
        self.pos = pos

        # Create the button rect.
        self.button_rect = pygame.Rect(0, 0, size[0], size[1])
        self.button_rect.center = (pos[0], pos[1])
        self.button_x = self.button_rect.x
        self.button_y = self.button_rect.y
        # Default button color.
        self.button_color = button_color
        # Current button color (changes on hover).
        self.current_button_color = button_color

        # Create the shadown rect.
        self.shadow_rect = pygame.Rect(0,0,size[0], size[1])
        self.shadow_rect.center = (pos[0]+shadow_size[0], pos[1]+shadow_size[1])
        # Shadow offset from the button.
        self.shadow_size = shadow_size
        # Shadow color.
        self.shadow_color = shadow_color

        # Border properties.
        # Border thickness (-1 for no border).
        self.border = border
        # Border color.
        self.border_color = border_color
        # Radius for rounded corners.
        self.border_radius = border_radius

        # Hover properties.
        # Color when the button is hovered.
        self.button_hover_color = button_hover_color
        # Text color when hovered.
        self.text_hover_color = text_hover_color
        # Stores the current text color.
        self.text_current_color = self.text_color
        # Transparency level (0 = opaque, -1 = fully transparent).
        self.transparency = transparency
        # Tracks whether the button is currently pressed.
        self.pressed = False
        self.visible = visible
        
    def draw(self, text):
        '''
        Draws the button on the screen.

        Parameters:
        - text: Text to display on the button.
        '''
        if self.visible:
            # Draw the shadow (background).
            pygame.draw.rect(self.screen, self.shadow_color, self.shadow_rect, border_radius=self.border_radius, width=self.transparency)
            # Draw the button (main rectangle).
            pygame.draw.rect(self.screen, self.current_button_color, self.button_rect, border_radius=self.border_radius, width=self.transparency)
            # Draw the border, if enabled.
            pygame.draw.rect(self.screen, self.border_color, self.button_rect, border_radius=self.border_radius, width=self.border)
            # Draw the text at the center of the button.
            self.write(text, (self.button_rect.centerx, self.button_rect.centery), self.button_rect.width)
    
    def click(self) -> bool:
        '''
        Handles mouse interaction with the button.

        Returns:
        - True if the button was clicked, False otherwise.
        '''
        if self.visible:
            # Get the current mouse position.
            mouse_pos = pygame.mouse.get_pos()
            # Adjust the button's clickable area based on the aspect ratio.
            updated_rect = pygame.Rect(self.button_x*self.aspect_ratio[0], self.button_y*self.aspect_ratio[1], self.button_rect.width*self.aspect_ratio[0], self.button_rect.height*self.aspect_ratio[1])
            # Check if the mouse is within the updated rectangle.
            if updated_rect.collidepoint(mouse_pos):
                # Change the button and text color for hover state.
                self.current_button_color = self.button_hover_color
                self.text_color = self.text_hover_color
                
                # Check if the left mouse button is pressed.
                if pygame.mouse.get_pressed()[0]:
                    # Move the button slightly to simulate a press (with shadow offset).
                    self.button_rect.center = (self.pos[0]+self.shadow_size[0], self.pos[1]+self.shadow_size[1])
                    self.pressed = True
                else:
                    # If the button was pressed and is now released, register a click.
                    if self.pressed:
                        # Reset button position.
                        self.button_rect.center = (self.pos[0], self.pos[1])
                        self.pressed = False
                        # Button click registered.
                        return True
            else:
                # Reset button state if the mouse is not over it.
                self.button_rect.center = (self.pos[0], self.pos[1])
                self.current_button_color = self.button_color
                self.text_color = self.text_current_color
                self.pressed = False
                # Button was not clicked.
                return False
        else:
            return False

class Slider(Button):
    def __init__(self, screen, aspect_ratio, pos, slider_value, size=(300, 30), multiplier=1, button_color = (100,100,100), button_hover_color = (100,100,100), border_radius = 20, padding = 20, pointer_radius = 8):
        '''
        Initializes the Slider object, which inherits from the Button class.

        Parameters:
        - screen: The Pygame screen to draw the slider on;
        - pos: Tuple containing the x and y position of the slider;
        - slider_value: Initial value of the slider (0 to 100);
        - size: Size of the slider as a tuple (width, height). Default is (300, 30);
        - multiplier: Multiplier for scaling the slider's value. Default is 1;
        - button_color: Color of the slider's button area. Default is (100, 100, 100);
        - button_hover_color: Hover color for the slider's button. Default is (100, 100, 100);
        - border_radius: Radius for the slider's button corners. Default is 20;
        - padding: Padding on the left and right sides of the slider. Default is 20;
        - pointer_radius: Radius of the slider pointer. Default is 8;
        - smooth: Boolean to determine if the slider moves smoothly or in discrete steps. Default is True.
        '''
        super().__init__(screen, aspect_ratio, pos, size, button_color=button_color, button_hover_color=button_hover_color, border_radius=border_radius)
        # Space on either side of the slider line.
        self.padding = padding
        # Size of the pointer (circle).
        self.pointer_radius = pointer_radius
        # Scaling factor for slider values.
        self.multiplier = multiplier
        # Calculate the initial pointer position based on the slider value.
        self.pointer_pos = int(((self.button_rect.width - self.padding*2) * slider_value / 100) / multiplier) + self.padding

    def draw_slider(self):
        '''
        Draws the slider on the screen.

        Draws the button using the parent draw method;
        Draws a horizontal line for the slider's track;
        Draws a circular pointer to represent the current slider value.
        '''
        # Draw the slider's button
        self.draw('')
        # Line width for the slider track.
        pygame.draw.line(self.screen, (0,0,0), (self.button_x + self.padding, self.button_y+self.button_rect.height/2), (self.button_rect.width - self.padding + self.button_x, self.button_rect.height/2 + self.button_y), width=2)
        # Draw the slider pointer as a circle
        pygame.draw.circle(self.screen, (0,0,0), (self.button_x + self.pointer_pos, self.button_y+self.button_rect.height/2), radius=self.pointer_radius)
    
    def click_slider(self):
        '''
        Handles mouse interaction with the slider.

        Returns:
        - True if the slider was clicked and value was updated;
        - False otherwise.
        '''
        # Get the current mouse position.
        mouse_pos = pygame.mouse.get_pos()
        # Adjust the slider's clickable area based on the aspect ratio.
        updated_rect = pygame.Rect((self.button_x + self.padding)*self.aspect_ratio[0], self.button_y*self.aspect_ratio[1], (self.button_rect.width-self.padding*2)*self.aspect_ratio[0], self.button_rect.height*self.aspect_ratio[1])
        # Check if the mouse is within the slider's clickable area.
        if updated_rect.collidepoint(mouse_pos):
            # Check if the left mouse button is pressed.
            if pygame.mouse.get_pressed()[0]:
                # Update the pointer position relative to the mouse.
                self.pointer_pos =  mouse_pos[0] - updated_rect.x
                # Calculate the slider value based on the pointer's position.
                self.slider_value = round((self.pointer_pos*100/updated_rect.width)*self.multiplier)
                self.pointer_pos = int(((self.button_rect.width - self.padding*2) * self.slider_value / 100) / self.multiplier) + self.padding
                # Slider value was updated.
                return True
        # Slider was not clicked or updated.
        return False

class TextBox(TextBoxContent):
    def __init__(self, screen, aspect_ratio, pos, size=(300, 100), visible=True, display_text='', text_padding=10, password=False, text_color=(0,0,0), display_text_color=(0,0,0), text_antialias=True, text_font=None, text_font_size=40, tb_color=(128,128,128), border=-1, border_color=(0,0,0), border_radius=0, transparency=0):
        '''
        Initializes the TextBox object, which is used for user text input.

        Parameters:
        - screen: The Pygame screen to display the text box on;
        - pos: Tuple containing the x and y position of the text box;
        - size: Size of the text box as a tuple (width, height). Default is (300, 100);
        - password: Boolean to determine if the text box hides the input (for passwords). Default is False;
        - text_color: Color of the text. Default is (0, 0, 0);
        - text_antialias: Boolean for text anti-aliasing. Default is True;
        - text_font: Font for the text. Default is None (uses Pygame default);
        - text_font_size: Size of the text font. Default is 40;
        - tb_color: Background color of the text box. Default is (128, 128, 128);
        - border: Thickness of the border around the text box. Default is -1 (no border);
        - border_color: Color of the border. Default is (0, 0, 0);
        - border_radius: Radius of the corners for the text box. Default is 0 (no rounding);
        - transparency: Transparency level of the text box. Default is 0 (fully opaque).
        '''
        super().__init__(screen, text_color, text_antialias, text_font, text_font_size)
        self.screen = screen
        self.aspect_ratio = aspect_ratio
        self.pos = pos
        # Text input by the user
        self.text = ''
        self.tb_rect = pygame.Rect(0, 0, size[0], size[1])
        self.tb_rect.center = (pos[0], pos[1])
        self.tb_x = self.tb_rect.x
        self.tb_y = self.tb_rect.y
        self.tb_color = tb_color
        self.border = border
        self.border_color = border_color
        self.border_radius = border_radius
        self.transparency = transparency
        self.pressed = False
        # Offset for text if it overflows the text box
        self.offset = 0
        # Whether the text box should hide input (password)
        self.password = password
        self.visible = visible
        self.display_text = display_text
        self.display_text_label = Label(screen, font_size=text_font_size, font=text_font, text_color=display_text_color)
        self.bar_text_label = Label(screen, font_size=text_font_size, font=text_font)
        self.text_padding = text_padding
        
    def draw(self):
        '''
        Draws the text box on the screen.

        Draws the text box background with a potential border, 
        then renders the user input (text or masked if password) inside it.
        '''
        if self.visible:
            # Draw the text box background and border
            pygame.draw.rect(self.screen, self.tb_color, self.tb_rect, border_radius=self.border_radius, width=self.transparency)
            pygame.draw.rect(self.screen, self.border_color, self.tb_rect, border_radius=self.border_radius, width=self.border)
            # Adjust text offset if it overflows the text box width
            if self.text_surf.get_width() > self.tb_rect.width:
                self.offset = self.text_surf.get_width() - self.tb_rect.width
            else:
                self.offset = 0
        
            # If the text box is set to password mode, display '*' for each character typed
            if self.password:
                self.write(f'{'*'*len(self.text)}', (self.tb_x, self.tb_y), self.offset, (self.tb_rect.width, self.tb_rect.height), self.text_padding)
            else:
                # Otherwise, display the actual user text
                self.write(self.text, (self.tb_x, self.tb_y), self.offset, (self.tb_rect.width, self.tb_rect.height), self.text_padding)
            
            # Blinking logic
            if self.text == '':
                self.display_text_label.write(self.display_text, (self.tb_x+self.text_padding, self.tb_y + self.tb_rect.height/3))
            if self.pressed:
                self.blink_time = pygame.time.get_ticks() - self.start_blink
                if self.blink_time <= 1000:
                    self.bar_text_label.write('|', (self.tb_x+self.text_surf.width+self.text_padding/2, self.tb_y + self.tb_rect.height/2), center_h=True)
                elif (self.blink_time//1000) % 2 == 0:
                    self.bar_text_label.write('|', (self.tb_x+self.text_surf.width+self.text_padding/2, self.tb_y + self.tb_rect.height/2), center_h=True)
            else:
                self.start_blink = pygame.time.get_ticks()
    
    def click(self):
        '''
        Handles mouse interaction with the text box.

        Returns:
        - True if the text box was clicked;
        - False otherwise.
        '''
        if self.visible:
            # Get the current mouse position
            mouse_pos = pygame.mouse.get_pos()
            # Adjust the text box rectangle for different screen aspect ratios
            updated_rect = pygame.Rect(self.tb_x*self.aspect_ratio[0], self.tb_y*self.aspect_ratio[1], self.tb_rect.width*self.aspect_ratio[0], self.tb_rect.height*self.aspect_ratio[1])
            # If the mouse click is within the text box, set the 'pressed' flag to True
            if updated_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif pygame.mouse.get_pressed()[0]:
                # If mouse is released outside, set the 'pressed' flag to False
                self.pressed = False
    
    def event(self, event):
        '''
        Handles keyboard events to capture user input when the text box is clicked.

        Parameters:
        - event: The Pygame event object that contains the keyboard input.

        Updates the user text based on key events (backspace, typing, etc.).
        '''
        # If the text box is pressed, process key events
        if self.pressed:
            if event.type == pygame.KEYDOWN:
                # Handle backspace key to delete last character
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Handle enter key to submit (currently does nothing)
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    # Add the character pressed to the user text
                    self.text += event.unicode

class Panel():
    def __init__(self, screen, aspect_ratio, pos, size=(100,100), color=(128,128,128)):
        self.screen = screen
        self.aspect_ratio = aspect_ratio
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.color = color
        self.panel_surf = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        self.acc = -10
    
    def draw(self):
        self.panel_surf.fill(self.color)
        self.screen.blit(self.panel_surf, self.pos)
    
    def update(self, dt):
        self.acceleration.x += self.acc * dt
        self.velocity += self.acceleration * dt
        self.pos += self.velocity * dt
