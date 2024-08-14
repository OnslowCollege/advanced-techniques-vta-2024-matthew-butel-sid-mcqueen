"""
Main.

Created by: Matthew Butel & Sid McQueen
Date: 17 June - Present
"""

# Imports
import remi.gui as GUI
from remi import start, App

from cars_db import Car, Cars
from users_db import User_Info, Users

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



class order_service():
    """."""

class services():
    """Manages database services"""

    users: Users = Users()
    cars: Cars = Cars()
    orders: order_service = order_service()


class UI(App):
    """The UI for the flash cards menu."""
    

    data: services = services()
    #logged_in_user: user_account = ()
    

    def __init__(self, *args):
        """Make the app work."""
        import os

        abs_path: str = os.path.abspath(__file__)
        dir_name: str = os.path.dirname(abs_path)
        res_path: str = os.path.join(dir_name, "res")
        super().__init__(*args, static_file_path={"res": res_path})
    
    def main(self) -> GUI.VBox:
        """GUI for the home screen."""
        self.cart_label = GUI.Label("")
        self.cart: list[Car] = []
        self.cart_price: int = 0
        self.ui_container: GUI.VBox = GUI.VBox()
        self.ui_container.append(self.home_screen())
        self.logged_in_user: User_Info = None
        return self.ui_container
    
    def home_screen(self):
        """GUI for the home screen"""
        
        # Create the features for the menu
        self.home_screen_title: GUI.Label = GUI.Label("Buy a Car you know you'll love")
        self.home_screen_title.style["height"] = "50px"
        self.image = GUI.Image("/res:car_logo.png")
        self.logotext = GUI.Label("AUTO BAZAAR")
        self.catalogue: GUI.Button = GUI.Button("Go to catalogue")
        self.account: GUI.Button = GUI.Button("Account settings")

        # Put them into H and VBox's
        self.buttons: GUI.HBox = GUI.VBox([self.catalogue, self.account])
        self.home_screen_final: GUI.VBox = GUI.VBox([self.home_screen_title, self.buttons])
        self.home_screen_logo: GUI.VBox = GUI.VBox([self.image, self.logotext])
        self.home_screen_: GUI.HBox = GUI.HBox([self.home_screen_logo, self.home_screen_final])
        
        self.account.onclick.do(self.account_page)
        self.catalogue.onclick.do(self.catalogue_page)
        return self.home_screen_
    
    def account_page(self, button: GUI.Button):
        if self.logged_in_user == None:
            self.signup_page(button)
            return

        self.ui_container.empty()
        username_display = GUI.Label(self.logged_in_user.username)
        hidden_number = (
            "**** **** **** " + self.logged_in_user.card_number[-4:]
        )
        private_card_number_dispay = GUI.Label(f"Card number: {hidden_number}")
        user_details = GUI.VBox(
            [username_display, private_card_number_dispay, self.catalogue]
        )
        self.ui_container.append(user_details)

        self.catalogue.onclick.do(self.catalogue_page)

    def signup_page(self, button: GUI.Button):
        """GUI for the account info page."""
        
        self.ui_container.empty()
        
        account_title: GUI.Label = GUI.Label("Account Details")
        self.error_message: GUI.Label = GUI.Label()
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
        self.catalogue_button.onclick.do(self.catalogue_page)

        
        
        button_box = GUI.HBox([self.return_button, self.catalogue_button])
        self.account_page_vbox = GUI.VBox(
            [
                self.logotext,
                account_title,
                user_name,
                card_details,
                self.signup_button,
                button_box,
                self.error_message,
                self.image,
            ]
        )
        self.ui_container.append(self.account_page_vbox)
        return self.ui_container

    def onclick_return(self, button: GUI.Button):
        """Return user to home screen."""

        self.ui_container.empty()
        self.ui_container.append(self.home_screen())
        

    def onclick_signup(self, button: GUI.Button):
        """Create a user account with validation."""

        # Check valid username
        username = self.name_input.get_value().strip()
        if not username:
            self.show_error("Username is required.")
            return
        if len(username) < 3:
            self.show_error("Username must be at least 3 characters long.")
            return

        # Check valid password
        password = self.password_input.get_value()
        if not password:
            self.show_error("Password is required.")
            return
        if len(password) < 8:
            self.show_error("Password must be at least 8 characters long.")
            return

        # Check valid card number
        card_number = self.number_input.get_value().replace(" ", "")
        if not card_number.isdigit() or len(card_number) != 16:
            self.show_error("Invalid card number. Must be 16 digits.")
            return

        # Check valid SCC
        scc = self.scc_input.get_value()
        if not scc.isdigit() or len(scc) != 3:
            self.show_error("Invalid SCC. Must be 3 digits.")
            return

        # Check Valid expiry date
        expire_date = self.expire_date_input.get_value()
        if not self.is_valid_expiry_date(expire_date):
            self.show_error("Invalid expiry date. Use MM/YY format.")
            return

        # Check Valid card name
        card_name = self.card_name_input.get_value().strip()
        if not card_name:
            self.show_error("Card name is required.")
            return

        # If all valid, create the user
        self.logged_in_user = User_Info(
            username=username,
            password=password,
            card_number=card_number,
            scc=int(scc),
            card_name=card_name,
            expire_date=expire_date,
        )

        try:
            self.data.users.add_user(self.logged_in_user)
            self.catalogue_page(button)
        except Exception as e:
            self.show_error(f"Error creating account: {str(e)}")

    def show_error(self, message: str):
        """Display an error message to the user."""
        self.error_message.set_text(message)
        self.error_message.style["color"] = "red"

    def is_valid_expiry_date(self, date_string: str) -> bool:
        """Check if the expiry date is valid (MM/YY format)."""
        import re
        from datetime import datetime

        if not re.match(r"^\d{2}/\d{2}$", date_string):
            return False

        month, year = map(int, date_string.split("/"))
        if month < 1 or month > 12:
            return False

        current_year = datetime.now().year % 100
        if year < current_year or year > current_year + 10:
            return False

        return True

    def catalogue_page(self, button: GUI.Button):
        """The catalogue for the site."""
        
        self.ui_container.empty()
        catalogue_title = GUI.Label("USED CAR CATALOGUE")
        catalogue_title_message = GUI.Label("Welcome to the Bazaar")

        title_hbox = GUI.HBox([self.logotext, catalogue_title])
        title = GUI.VBox([title_hbox, catalogue_title_message])

        view_cart = GUI.Button("View Cart")
        return_button = GUI.Button("Return to Home")
        button_box = GUI.VBox([self.account, return_button, view_cart])

        upper_page = GUI.HBox([title, button_box])

        catalogue: list[Car] = self.data.cars.get_cars()
        catalogue_box = GUI.VBox([])

        for car in catalogue:
            place_holder_car = GUI.Label(repr(car))
            car_price = GUI.Label("$" + repr(car.price))
            add_to_cart = GUI.Button("Add To Cart")
            car_row = GUI.HBox([place_holder_car, car_price, add_to_cart])
            catalogue_box.append(car_row)
            add_to_cart.onclick.do(self.onclick_addtocart)
            add_to_cart.car = car

        self.account.onclick.do(self.account_page)
        return_button.onclick.do(self.onclick_return)
        view_cart.onclick.do(self.view_cart_page)

        self.catalogue_page_vbox = GUI.VBox([upper_page, catalogue_box])
        self.ui_container.empty()
        self.ui_container.append(self.catalogue_page_vbox)
        return self.catalogue_page_vbox

    def onclick_addtocart(self, button: GUI.Button):
        """When the user presses add to cart, add to cart."""

        self.cart.append(button.car)
    
    def view_cart_page(self, button: GUI.Button):
        """When the user chooses to view cart open they go to this page."""

        self.cart_price = 0
        cart_title = GUI.Label("Your Cart")
        cart_vbox = GUI.VBox()
        for car in self.cart:
            car_in_cart = GUI.Label(repr(car))
            self.cart_price = self.cart_price + int(repr(car.price))
            remove_from_cart_button = GUI.Button("Remove From Cart")
            remove_from_cart_button.onclick.do(self.onclick_removefromcart)
            remove_from_cart_button.car = car
            cart_hbox: GUI.HBox = GUI.HBox([car_in_cart, remove_from_cart_button])
            cart_vbox.append(cart_hbox)

        price_label = GUI.Label("Total Cost: $" + str(self.cart_price))
        purchase_button = GUI.Button("Purchase")
        back_button = GUI.Button("Back To Catalogue")
        button_row = GUI.HBox([purchase_button, back_button])
        view_cart_vbox = GUI.VBox([cart_title, price_label, cart_vbox, button_row])
        back_button.onclick.do(self.catalogue_page)
        self.ui_container.empty()
        self.ui_container.append(view_cart_vbox)

    def onclick_removefromcart(self, button: GUI.Button):
        """Remove item from cart."""

        self.cart.remove(button.car)

        self.view_cart_page(button)


start(UI)