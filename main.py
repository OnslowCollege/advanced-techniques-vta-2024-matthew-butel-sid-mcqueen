"""
Main.

Created by: Matthew Butel & Sid McQueen
Date: 17 June - Present
"""

# Imports
import remi.gui as GUI
from remi import start, App

import re
from datetime import datetime

from cars_db import Car, Cars
from users_db import User_Info, Users
from orders_db import Order, Orders

# Service class
class services():
    """Manages database services."""

    users: Users = Users()
    cars: Cars = Cars()
    orders: Orders = Orders()


# Class for the UI
class UI(App):
    """The UI for the website."""

    data: services = services()

    def __init__(self, *args):
        """Make the app work."""
        import os

        abs_path: str = os.path.abspath(__file__)
        dir_name: str = os.path.dirname(abs_path)
        res_path: str = os.path.join(dir_name, "res")
        super().__init__(*args, static_file_path={"res": res_path})

    # Set up components for the site and then show the home screen
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
        """GUI for the home screen."""

        # Create the features for the menu
        self.home_screen_title: GUI.Label = GUI.Label(
            "Buy a Car you know you'll love"
        )
        self.home_screen_title.style["height"] = "50px"
        self.image = GUI.Image("/res:car_logo.png")
        self.logotext = GUI.Label("AUTO BAZAAR")
        self.catalogue: GUI.Button = GUI.Button("Go to catalogue")
        self.account: GUI.Button = GUI.Button("Account settings")

        # Put them into H and VBox's
        self.buttons: GUI.HBox = GUI.VBox([self.catalogue, self.account])
        self.home_screen_final: GUI.VBox = GUI.VBox(
            [self.home_screen_title, self.buttons]
        )
        self.home_screen_logo: GUI.VBox = GUI.VBox([self.image, self.logotext])
        self.home_screen_: GUI.HBox = GUI.HBox(
            [self.home_screen_logo, self.home_screen_final]
        )

        # On click funtions for the buttons
        self.account.onclick.do(self.account_page)
        self.catalogue.onclick.do(self.catalogue_page)
        return self.home_screen_

    # When the user presses account page show this page
    def account_page(self, button: GUI.Button):
        """Check wether use is signed in or not the runs the correct page."""
        if self.logged_in_user == None:
            self.signup_page(button)
            return

        # Empty the screen then add the appropriate user details
        self.ui_container.empty()
        username_display = GUI.Label(
            "Username: " + self.logged_in_user.username
        )

        private_card_number_dispay = GUI.Label(
            f"Card number: {self.logged_in_user.hidden_number()}"
        )
        user_details = GUI.VBox(
            [username_display, private_card_number_dispay, self.catalogue]
        )
        self.ui_container.append(user_details)

        self.catalogue.onclick.do(self.catalogue_page)

    # If the user isn't signed in this is the page they will get
    def signup_page(self, button: GUI.Button):
        """GUI for the account info page."""

        # Empty the screen
        self.ui_container.empty()

        # Create all the name components
        account_title: GUI.Label = GUI.Label("Account Details")
        self.error_message: GUI.Label = GUI.Label()
        username_question = GUI.Label("Username here")
        self.name_input = GUI.TextInput()
        user_password = GUI.Label("Password here")
        self.password_input = GUI.TextInput()

        # But them in an HBox
        user_name = GUI.HBox(
            [
                username_question,
                self.name_input,
                user_password,
                self.password_input,
            ]
        )

        # Create all the card details variables
        card_detail_title = GUI.Label("Enter Card Details Below")
        card_number = GUI.Label("Card Number:")
        self.number_input = GUI.TextInput()
        card_scc = GUI.Label("SCC:")
        self.scc_input = GUI.TextInput()
        expire_date = GUI.Label("Expiry date: ")
        self.expire_date_input = GUI.TextInput()

        # Put these in a Hbox
        card_number_row = GUI.HBox(
            [card_scc, self.scc_input, expire_date, self.expire_date_input]
        )

        # Card name
        card_name = GUI.Label("Name on Card:")
        self.card_name_input = GUI.TextInput()
        card_name_row = GUI.HBox([card_name, self.card_name_input])

        # Add all the components to a Vbox
        card_details = GUI.VBox(
            [
                card_detail_title,
                card_number,
                self.number_input,
                card_number_row,
                card_name_row,
            ]
        )

        # Buttons for this page
        self.signup_button = GUI.Button("Sign up")
        self.return_button = GUI.Button("Return To Home Screen")
        self.catalogue_button = GUI.Button("Proceed To Catalogue")

        # On click for each button
        self.signup_button.onclick.do(self.onclick_signup)
        self.return_button.onclick.do(self.onclick_return)
        self.catalogue_button.onclick.do(self.catalogue_page)

        # Put all the components of the UI together
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

        # Show the UI
        self.ui_container.append(self.account_page_vbox)
        return self.ui_container

    # Return's user to the home screen
    def onclick_return(self, button: GUI.Button):
        """Return user to home screen."""

        self.ui_container.empty()
        self.ui_container.append(self.home_screen())

    # Starts all the validation checks and if all goes smoothly creates a user
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
            self.show_error(
                "Invalid expiry date. Use MM/YY format. Use Valid Dates."
            )
            return

        # Check Valid card name
        card_name = self.card_name_input.get_value().strip()
        if not card_name:
            self.show_error("Card name is required.")
            return

        # If all valid, create the user
        user = User_Info(
            username=username,
            password=password,
            card_number=card_number,
            scc=int(scc),
            card_name=card_name,
            expire_date=expire_date,
        )

        try:
            self.logged_in_user = self.data.users.add_user(user)
            self.catalogue_page(button)
        except Exception as e:
            self.show_error(f"Error creating account: {str(e)}")

    # Prints an error message if there is something wrong
    def show_error(self, message: str):
        """Display an error message to the user."""
        self.error_message.set_text(message)
        self.error_message.style["color"] = "red"

    # Special code to check valid expiry date
    # This code will check the format and then if the date are not in the past
    # or too far in the future
    def is_valid_expiry_date(self, date_string: str) -> bool:
        """Check if the expiry date is valid (MM/YY format)."""

        if not re.match(r"^\d{2}/\d{2}$", date_string):
            return False

        month, year = map(int, date_string.split("/"))
        if month < 1 or month > 12:
            return False

        current_year = datetime.now().year % 100
        if year < current_year or year > current_year + 10:
            return False

        return True

    # The catalogue page
    def catalogue_page(self, button: GUI.Button):
        """Catalogue for the site."""

        self.ui_container.empty()

        # Titles for the catalogue
        catalogue_title = GUI.Label("USED CAR CATALOGUE")
        catalogue_title_message = GUI.Label("Welcome to the Bazaar")

        # Put them in boxes
        title_hbox = GUI.HBox([self.logotext, catalogue_title])
        title = GUI.VBox([title_hbox, catalogue_title_message])

        # Second menu with buttons
        view_cart = GUI.Button("View Cart")
        return_button = GUI.Button("Return to Home")
        button_box = GUI.VBox([self.account, return_button, view_cart])

        # Create filters
        # Transmission filter
        filter_transmission_label = GUI.Label("Filter Transmission:")
        transmission_filter_options: list[str] = ["All", "Automatic", "Manual"]
        self.transmission_filter = GUI.DropDown(transmission_filter_options)
        self.transmission_filter.set_value("All")
        transmission_filter_all = GUI.VBox(
            [filter_transmission_label, self.transmission_filter]
        )

        # Car make filter
        make_filter_label = GUI.Label("Filter Make:")
        make_filter_options: list[str] = [
            "All",
            "Alfa Romeo",
            "Audi",
            "BMW",
            "Ford",
            "Holden",
            "Honda",
            "Hyundai",
            "Jeep",
            "Kia",
            "Mazda",
            "Mercedes-Benz",
            "MG",
            "Mitsubishi",
            "Nissan",
            "Ssangyong",
            "Subaru",
            "Suzuki",
            "Toyota",
            "VolksWagen",
        ]
        self.make_filter = GUI.DropDown(make_filter_options)
        self.make_filter.set_value("All")
        make_filter_all = GUI.VBox([make_filter_label, self.make_filter])

        # Filter update button
        filter_confirm = GUI.Button("Update")
        filter_hbox = GUI.HBox(
            [
                transmission_filter_all,
                make_filter_all,
                filter_confirm,
            ]
        )
        filter_confirm.onclick.do(self.load_catalogue)

        # Put all the components into a single vbox
        menus = GUI.HBox([title, button_box])
        upper_page = GUI.VBox([menus, filter_hbox])

        self.catalogue_box = GUI.VBox([])

        # Load the catalogue
        self.load_catalogue()

        # All the onclick's for the menu buttons
        self.account.onclick.do(self.account_page)
        return_button.onclick.do(self.onclick_return)
        view_cart.onclick.do(self.view_cart_page)

        # Show the UI
        self.catalogue_page_vbox = GUI.VBox([upper_page, self.catalogue_box])
        self.ui_container.empty()
        self.ui_container.append(self.catalogue_page_vbox)
        return self.catalogue_page_vbox

    # Loads the catalogue
    def load_catalogue(self, button: GUI.Button = None):
        """Load the catalogue of cars with all the information."""
        self.catalogue_box.empty()

        # Check for filters
        transmission = self.transmission_filter.get_value()
        make = self.make_filter.get_value()

        # Get car data
        catalogue: list[Car] = self.data.cars.get_cars(transmission, make)

        # For loop to create all the cars in the catalogue
        for car in catalogue:
            # Relevant information
            catalogue_car = GUI.Label(repr(car))
            car_price = GUI.Label(f"${repr(car.price)}")
            car_mileage = GUI.Label(f"{repr(car.mileage)}km")
            car_button: GUI.Button

            # Style to evenly space the information
            catalogue_car.style["width"] = "250px"
            car_mileage.style["width"] = "80px"
            car_price.style["width"] = "80px"

            # If the car is in the cart switch the button
            if self.is_car_in_cart(car):
                car_button = GUI.Button("In Cart")
                car_button.set_enabled(False)

            # If its not use the normal add to cart button
            else:
                car_button = GUI.Button("Add To Cart")
                car_button.onclick.do(self.onclick_addtocart)
                car_button.car = car
                car_button.style["padding"] = "5px"

            # Hbox's for each individual car
            car_row = GUI.HBox(
                [catalogue_car, car_mileage, car_price, car_button]
            )

            # Adds the car to the UI
            self.catalogue_box.append(car_row)

    # A bool for wether the car is in the cart or not
    def is_car_in_cart(self, car: Car) -> bool:
        """Return a bool indicating whether the car is in the cart."""
        return any(cart_car.ids == car.ids for cart_car in self.cart)

    # Add the car to cart when the user presses the button
    def onclick_addtocart(self, button: GUI.Button):
        """When the user presses add to cart, add to cart."""

        self.cart.append(button.car)
        self.load_catalogue(button)

    # The View Cart Page
    def view_cart_page(self, button: GUI.Button):
        """When the user chooses to view cart open they go to this page."""

        self.cart_price = 0
        cart_title = GUI.Label("Your Cart")
        cart_vbox = GUI.VBox()

        # For loop for each car in the cart
        for car in self.cart:
            # Add the car
            car_in_cart = GUI.Label(repr(car))
            # Add the price
            self.cart_price = self.cart_price + int(repr(car.price))
            # Make a remove from cart button
            remove_from_cart_button = GUI.Button("Remove From Cart")
            remove_from_cart_button.onclick.do(self.onclick_removefromcart)
            remove_from_cart_button.car = car
            # Put them all in a box
            cart_hbox: GUI.HBox = GUI.HBox(
                [car_in_cart, remove_from_cart_button]
            )
            # Add to the UI
            cart_vbox.append(cart_hbox)

        # Labels and buttons
        price_label = GUI.Label("Total Cost: $" + str(self.cart_price))
        purchase_button = GUI.Button("Purchase")
        back_button = GUI.Button("Back To Catalogue")

        # Add them to box's
        button_row = GUI.HBox([purchase_button, back_button])
        view_cart_vbox = GUI.VBox(
            [cart_title, price_label, cart_vbox, button_row]
        )

        # On click's for the buttons
        back_button.onclick.do(self.catalogue_page)
        purchase_button.onclick.do(self.on_click_purchase)

        # Showing the UI
        self.ui_container.empty()
        self.ui_container.append(view_cart_vbox)

    # When the user presses remove from cart
    def onclick_removefromcart(self, button: GUI.Button):
        """Remove item from cart."""

        self.cart.remove(button.car)
        self.view_cart_page(button)

    # The user presses purchase
    def on_click_purchase(self, button: GUI.Button):
        """Begin the purchase sequence."""

        # Check if the user is signed up and if they're not make them
        if self.logged_in_user == None:
            self.signup_page(button)
            return

        # What's in an order
        order = Order(
            date=datetime.today(),
            user=self.logged_in_user,
            total_price=self.cart_price,
        )

        # Record order then show thank you page
        order = self.data.orders.add_order_with_cars(order, self.cart)
        self.cart = []
        self.logged_in_user = self.data.users.get_user(order.user_id)
        self.thank_you_page(order)

    # Show the thank you page
    def thank_you_page(self, order: Order):
        """Finalise purchase."""

        # Show a clear thank you message
        thank_you_message = GUI.Label("Thank you for shopping at Auto Bazaar")

        # Show what cars the user bought
        your_order_label = GUI.Label("You have purchased these cars:")
        final_purchase_vbox: GUI.VBox = []
        for car in order.cars:
            car_in_cart = GUI.Label(repr(car))
            final_purchase_vbox.append(car_in_cart)

        # Show the total price
        total_price_message = GUI.Label(
            "The total price of your order is $" + str(order.total_price)
        )

        # And lastly show the card it will be charged to
        card_charge_message = GUI.Label(
            "This will be charged to the following card: "
            + order.user.hidden_number()
        )
        thank_you_page_vbox = GUI.VBox(
            [
                thank_you_message,
                your_order_label,
                final_purchase_vbox,
                total_price_message,
                card_charge_message,
                self.image,
            ]
        )

        # Show the UI
        self.ui_container.empty()
        self.ui_container.append(thank_you_page_vbox)

# Run the code
start(UI)