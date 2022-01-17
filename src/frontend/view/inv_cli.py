import uuid

import requests

from src.frontend.frontend_utils.constants import *
from src.backend.controller.controller import InvController

from src.backend.model.model import InvModel
from src.frontend.frontend_utils.IOUtils import get_yn


class InvCLI:

    def __init__(self):
        self.choices = main_menu_options

    def checkConnection(self):
        response = requests.get('http://localhost:8000/').json()
        print(response['message'], '\n')

        return response


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

        prod_details = {}
        print("Enter the product details as prompted below")
        print("*******************************************")

        r = requests.get('https://localhost:8000/categories')
        print(type(r))

        print()
        print("PRODUCT CATEGORY")
        if get_yn("Create new category? Y/N:"):
            prod_details['category'] = input("Input category name: ")
        else:
            prod_details['category'] ="guitars"

        print()
        print("PRODUCT ID")
        print("Generating dummy product ID")
        prod_details['prod_id'] = uuid.uuid4()

        print()
        print("PRODUCT NAME")
        prod_details['prod_name'] = input("Input product name: ")

        print()
        print("PRODUCT PRICE")
        prod_details['prod_price'] = input("Enter store price of the item in USD: ")

        print()
        print("PRODUCT DESCRIPTION")
        print("Generating a dummy description for the product")
        prod_details['prod_price'] = "Solid spruce top. Mahogany laminate back and sides."

        response = requests.post('http://localhost:8000/product', json=prod_details)
        if response.json()['success_code'] == 1:
            print("Product successfully inserted")
            return 1
        elif response.json()['success_code'] == 2:
            print("Product ID already exists. No additions made.")
            return 0
        else:
            print("Insertion failed")
            return 0

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
