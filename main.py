"""
Main.

Created by: Matthew Butel & Sid McQueen
Date: 17 June - Present
"""

# Imports
import remi.gui as GUI
from remi import start, App

class user_account():
    """Stores account details."""

    def __init__(self, username, password, card_number, scc, expire_date, card_name):
        """."""

        self.username: str = username
        self.password: str = password
        self.cardnumber : str = card_number
        self.scc: int = scc
        self.cardname: str = card_name
        self.expiry_date: str = expire_date


class user_service():
    """List of user accounts."""

    # Change this to be a database later.
    accounts: list[user_account] = []

    def sign_up(self, username, password, card_number, scc, expire_date, card_name):
        """Take all the feilds and make a new account."""

        user = user_account(username, password, card_number, scc, expire_date, card_name)
        self.accounts.append(user)
        return user


    def sign_in():
        """Takes username and password and returns account."""

class car_service():
    """."""

class order_service():
    """."""

class services():
    """Manages database services"""

    users: user_service = user_service()
    cars: car_service = car_service()
    orders: order_service = order_service()


class UI(App):
    """The UI for the flash cards menu."""
    
    data: services = services()
    logged_in_user: user_account = ()

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
        
        #self.account_title: GUI.Label = GUI.Label("")
        #self.account_title.set_text("Account Details")
        #self.account_title.style["height"] = "50px"
        
        username_question = GUI.Label("Username here")
        self.name_input = GUI.TextInput()
        user_password = GUI.Label("Password here")
        self.password_input = GUI.TextInput()
        user_name = GUI.HBox([username_question, self.name_input, user_password, self.password_input])

        card_detail_title = GUI.Label("Enter Card Details Below")
        card_number = GUI.Label("Card Number:")
        self.number_input = GUI.TextInput()
        card_scc = GUI.Label("SCC:")
        self.scc_input = GUI.TextInput()
        expire_date = GUI.Label("Expiry date: ")
        self.expire_date_input = GUI.TextInput()
        card_number_row = GUI.HBox([card_scc, self.scc_input, expire_date, self.expire_date_input])
        card_name = GUI.Label("Name on Card:")
        self.card_name_input = GUI.TextInput()
        card_name_row = GUI.HBox([card_name, self.card_name_input])
        
        card_details = GUI.VBox([card_detail_title, card_number, self.number_input, card_number_row, card_name_row])

        self.signup_button = GUI.Button("Sign up")
        self.return_button = GUI.Button("Return To Home Screen")
        self.catalogue_button = GUI.Button("Proceed To Catalogue")

        self.signup_button.onclick.do(self.onclick_signup)
        self.return_button.onclick.do(self.onclick_return)

        
        
        button_box = GUI.HBox([self.return_button, self.catalogue_button])
        self.account_page_vbox = GUI.VBox([self.logotext, user_name, card_details, self.signup_button, button_box, self.image])
        self.ui_container.append(self.account_page_vbox)
        return self.ui_container

    def onclick_return(self, button: GUI.Button):
        """Return user to home screen."""

        self.ui_container.empty()
        self.ui_container.append(self.home_screen())

    def onclick_signup(self, button: GUI.Button):
        """Create a user account."""

        username = self.name_input.get_value()
        password = self.password_input.get_value()
        card_number = self.number_input.get_value()
        scc = self.scc_input.get_value()
        expire_date = self.expire_date_input.get_value()
        card_name = self.card_name_input.get_value()
        self.logged_in_user = self.data.users.sign_up(username, password, card_number, scc, expire_date, card_name)


start(UI)