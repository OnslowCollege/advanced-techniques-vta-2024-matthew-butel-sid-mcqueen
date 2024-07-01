"""
Main.

Created by: Matthew Butel & Sid McQueen
Date: 17 June - Present
"""

# Imports
import remi.gui as GUI
from remi import start, App


class UI(App):
    """The UI for the flash cards menu."""
    
    def __init__(self, *args):
        """Make the app work."""
        import os

        abs_path: str = os.path.abspath(__file__)
        dir_name: str = os.path.dirname(abs_path)
        res_path: str = os.path.join(dir_name, "res")
        super().__init__(*args, static_file_path={"res": res_path})
    
    def main(self):
        """Run the site."""
        return self.home_screen()
    
    def home_screen(self):
        """GUI for the home screen"""
        
        self.home_screen_title: GUI.Label = GUI.Label("Wheels & Deals")
        self.go_to_catalogue: GUI.Button = GUI.Button("Go to Catalogue")
        self.create_account: GUI.Button = GUI.Button("Create an Account")
        self.button_row: GUI.HBox = GUI.HBox([self.go_to_catalogue, self.create_account])
        self.home_screen_final: GUI.VBox = GUI.VBox([self.home_screen_title, self.button_row])

        return self.home_screen_final

start(UI)