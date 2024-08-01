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
        self.logotext: GUI.Label = GUI.Label("AUTO BAZAAR")
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
        
        account_title: GUI.Label = GUI.Label("")
        account_title.set_text("Account Details")
        account_title.style["height"] = "50px"
        
        user_name_question = GUI.Label("First and Last name here")
        name_input = GUI.TextInput()
        user_name = GUI.HBox([user_name_question, name_input])

        card_detail_title = GUI.Label("Enter Card Details Below")
        card_number = GUI.Label("Card Number:")
        number_input = GUI.TextInput()
        card_scc = GUI.Label("SCC:")
        scc_input = GUI.TextInput()
        card_number_row = GUI.HBox([card_number, number_input, card_scc, scc_input])
        card_name = GUI.Label("Name on Card:")
        card_name_input = GUI.TextInput()
        card_name_row = GUI.HBox([card_name, card_name_input])
        
        card_details = GUI.VBox([card_detail_title, card_number_row, card_name_row])

        self.return_button = GUI.Button("Return To Home Screen")
        self.catalogue_button = GUI.Button("Proceed To Catalogue")
        self.catalogue_button.set_enabled(False)

        self.return_button.onclick.do(self.onclick_return)

        number_input.onchange.do(self.onchange_card_details)
        scc_input.onchange.do(self.onchange_card_details)
        card_name_input.onchange.do(self.onchange_card_details)
        
        button_box = GUI.HBox([self.return_button, self.catalogue_button])
        self.account_page_vbox = GUI.VBox([self.logotext, account_title, user_name, card_details, button_box, self.image])
        self.ui_container.append(self.account_page_vbox)
        return self.ui_container

    def onclick_return(self, button: GUI.Button):
        """Return user to home screen."""

        self.ui_container.empty()
        self.ui_container.append(self.home_screen())

    def onchange_card_details(self):
        """Make the catalogue button pressable once the user enters card details."""

        
start(UI)