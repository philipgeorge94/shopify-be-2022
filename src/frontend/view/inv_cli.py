import requests

from src.frontend.utils.constants import *
from src.backend.controller.controller import InvController

from src.backend.model.model import InvModel
from src.frontend.utils.IOUtils import get_yn


class InvCLI:

    def __init__(self):
        self.choices = main_menu_options
        self.invController = InvController(InvModel())

    def display_main_menu(self):
        # Main menu options
        print("Main Menu: ")
        print("1. Add a product to inventory")
        print("2. View products")
        print("3. Update existing product details")
        print("4. Delete product")
        print()
        user_choice = int(input("Enter choice: "))

        return user_choice

    def initiate_create_product(self):
        print("Enter the product details as prompted below")
        print("*******************************************", '\n')

        r = requests.get('https://localhost:8000/categories')
        print (type(r))

        print("PRODUCT CATEGORY")
        if get_yn("Create new category? Y/N:"):
            category = input("Input category name: ")


        pass

    def execute_user_command(self, command):
        if command < 1 or command > 4:
            print("Not a valid command")
            print()
            flow = None
            return
        if command == 1:
            flow = self.initiate_create_product()
        elif command == 2:
            flow = self.initiate_delete_product()
        elif command == 3:
            flow = self.initiate_update_product()
        elif command == 4:
            flow = self.initiate_view_product()

        if not flow():
            print(" the user command was not executed", '\n')

        return

    if __name__ == 'main':
        app = InvCLI()
        while (choice := app.display_main_menu()) > 0:
            app.execute_user_command(choice)
        print(["X"] * 20)
        print("Terminal shut down.")
        print(["X"] * 20)
    # print(uuid4(now))
