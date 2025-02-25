import json
import os

class Settings():
    '''
    Manages game settings stored in a JSON file.
    Provides functionality to load, update, and retrieve settings.
    '''
    def __init__(self):
        '''
        Initializes the Settings class:

        - Defines the path to the settings JSON file;
        - Loads settings from the file into memory;
        - Initializes game-specific settings.
        '''
        # Define the base path of the project directory.
        self.path = os.path.join(os.path.dirname(__file__), '..', '..')
        # Define the path to the settings.json file located in the 'config' directory.
        self.file_path = os.path.join(self.path, 'config', 'settings.json')
        # Load the settings from the JSON file.
        self.settings = self.load_settings()
        # Initialize game-specific settings.
        self.game_settings()
    
    def load_settings(self):
        '''
        Loads settings from the JSON file.

        Returns:
        - A dictionary containing the settings loaded from the file.
        '''
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def game_settings(self):
        '''
        Initializes game-related settings by extracting values from the loaded settings.

        Creates attributes for:
        - Video settings;
        - Audio settings;
        - Language settings;
        - Game text based on the selected language;
        - Game data;
        - Controls.
        '''
        # Load specific categories of settings.
        # Video-related settings.
        self.video_settings = self.get_settings('video')
        # Audio-related settings.
        self.audio_settings = self.get_settings('audio')
        # Language settings.
        self.language = self.get_settings('language')
        # Get the current language set.
        self.language_set = self.language['language_set']
        # Load game texts corresponding to the selected language.
        self.game_texts = self.language[self.language_set]
        # Load other game-related settings.
        self.game_data = self.get_settings('game_data')
        self.controls = self.get_settings('keys')
    
    def update_settings(self):
        '''
        Updates the JSON file with the current settings in memory.
        Also reinitializes the game settings after updating the file.
        '''
        with open(self.file_path, 'w', encoding='utf-8') as file:
            # Write the current settings dictionary to the file with indentation.
            json.dump(self.settings, file, indent=4, ensure_ascii=False)
        # Reinitialize game settings to reflect the updated values.
        self.game_settings()

    def get_settings(self, key):
        '''
        Retrieves a specific setting value by its key.

        Parameters:
        - key: The key corresponding to the desired setting.

        Returns:
        - The value associated with the provided key.
        '''
        return self.settings.get(key)
    
    def set_settings(self, option, key, value):
        '''
        Updates a specific setting value and saves the changes to the JSON file.

        Parameters:
        - option: The top-level category in the settings dictionary;
        - key: The specific key within the category to update;
        - value: The new value to set for the key.
        '''
        # Update the value of the specified key in the settings dictionary.
        self.settings[option][key] = value
        # Save the updated settings to the JSON file.
        self.update_settings()
