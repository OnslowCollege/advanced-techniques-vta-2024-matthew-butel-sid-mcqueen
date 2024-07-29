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
    
    def main(self) -> GUI.VBox:
        """GUI for the home screen."""
        self.ui_container: GUI.VBox = GUI.VBox()
        self.ui_container.append(self.home_screen())
        return self.ui_container
    
    def home_screen(self):
        """GUI for the home screen"""
        
        # Create the features for the menu
        self.home_screen_title: GUI.Label = GUI.Label("Buy a Car you know you'll love")
        self.home_screen_title.style["height"] = "50px"
        self.image = GUI.Image("/res:car_logo.png")
        self.logotext = GUI.Label = GUI.Label("AUTO BAZAAR")
        self.catalogue: GUI.Button = GUI.Button("Go to catalogue")
        self.account: GUI.Button = GUI.Button("Account settings")
        
        # Put them into H and VBox's
        self.buttons: GUI.HBox = GUI.VBox([self.catalogue, self.account])
        self.home_screen_final: GUI.VBox = GUI.VBox([self.home_screen_title, self.buttons])
        self.home_screen_logo: GUI.VBox = GUI.VBox([self.image, self.logotext])
        self.home_screen_: GUI.HBox = GUI.HBox([self.home_screen_logo, self.home_screen_final])
        
        self.catalogue.set_enabled(False)

        self.account.onclick.do(self.account_page)
        # self.catalogue.onclick.do(self.catalogue_page)
        return self.home_screen_
    
    def account_page(self, button: GUI.Button):
        """GUI for the account info page"""
        
        self.ui_container.empty()
        
        self.account_title = GUI.Label("")
        self.account_title.get_text("Account Details")
        self.account_title.style["height"] = "50px"
        
        self.name_input = GUI.TextInput("First and Last Name")

        self.return_button = GUI.Button("Return To Home Screen")
        self.catalogue_button = GUI.Button("Proceed To Catalogue")
        self.catalogue_button.set_enabled(False)
        self.button_box = GUI.HBox([self.return_button, self.catalogue_button])
        self.account_page_vbox = GUI.VBox([self.account_title, self.name_input, self.button_box])
        self.ui_container.append(self.account_page_vbox)
        return self.ui_container

start(UI)