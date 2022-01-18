import json
import uuid
import requests
from src.frontend.frontend_utils.constants import *
from src.frontend.frontend_utils.frontend_utils import get_yn, refresh_prod_lookups


class InvCLI:

    def __init__(self):
        self.url = 'http://localhost:8000/'
        self.check_connection()
        self.choices = main_menu_options
        self.prod_ids = refresh_prod_lookups(self.retrieve_products('all'))

    def retrieve_products(self, prod_id):
        response = requests.get(self.url + 'product/' + prod_id).json()
        return response['message'], int(response['success_code']), response['prods_data']

    def check_connection(self):
        response = requests.get(self.url).json()
        print(response['message'], '\n')

        return response

    def display_main_menu(self):
        # Main menu options
        print()
        print("Main Menu: ")
        print("1. Add a product to inventory")
        print("2. View products")
        print("3. Update existing product details")
        print("4. Delete product")
        print("0. Close program")
        print()
        user_choice = int(input("Enter choice: "))

        return user_choice

    def create_product_menu(self):

        prod_details = {}
        print("Enter the product details as prompted below")
        print("*******************************************")

        print()
        print("PRODUCT ID")
        # prod_details['prod_id'] = str(uuid.uuid4())
        # print("Generating dummy product ID " + prod_details['prod_id'])
        prod_details['prod_id'] = input("Enter product ID: ")
        if prod_details['prod_id'].lower() == 'all':
            print()
            print("Invalid ID. 'All' is a reserved keyword.")
            return False
        if prod_details['prod_id'] in self.prod_ids:
            print()
            print("This product ID already exists in the database at db_id = " + self.prod_ids[prod_details['prod_id']])
            return False

        print()
        print("PRODUCT NAME")
        prod_details['prod_name'] = input("Input product name: ")

        print()
        print("PRODUCT PRICE")
        prod_details['prod_price'] = input("Enter store price of the item in USD: ")

        print()
        print("PRODUCT DESCRIPTION")
        print("Generating a dummy description for the product")
        prod_details['prod_desc'] = "Solid spruce top. Mahogany laminate back and sides."

        print()
        print("PRODUCT QUANTITY")
        prod_details['prod_qty'] = input("Enter product quantity: ")

        # print(prod_details)
        response = requests.post(self.url + 'product', data=prod_details).json()
        success_code = int(response['success_code'])

        if success_code == 1:
            print()
            print(response['message'] + ' with db_id = ' + response['id'])
            self.prod_ids[prod_details['prod_id']] = response['id']
            return True

        print()
        print(response['message'])
        return False

    def delete_product_menu(self):
        print()
        prod_id = input("Enter product ID of product to be deleted: ")

        if prod_id not in self.prod_ids:
            print()
            print("This product ID doesn't exist in the database")
            return False
        response = requests.delete(self.url + 'product/' + prod_id).json()
        success_code = int(response['success_code'])
        if success_code == 1:
            print()
            print(response['message'] + ' at db_id = ' + response['id'])
            del self.prod_ids[prod_id]
            return True
        print()
        print(response['message'])
        return False

    def view_product_menu(self):
        print()
        prod_id = input("Enter prod_id to view or 'all' to view all products: ").lower()
        if prod_id != 'all' and prod_id not in self.prod_ids:
            print("This product doesn't exist in the database")
            return False
        message, success_code, prods_data = self.retrieve_products(prod_id)
        if not prods_data:
            print()
            print("No products to display")
            return True

        if success_code == 1:
            print()
            print(str(len(prods_data)) + ' product(s) retrieved. Printing...')
            print()
            for prod in prods_data:
                prod_str = []
                for key, value in prod.items():
                    prod_str.append(key + " = " + value)
                print(" | ".join(prod_str[1:]))
            return True
        else:
            print(message)
            return False

    def update_field_menu(self, prod):
        while True:
            print()
            print("Editing product " + prod['prod_id'])
            print("Enter number indicating field you want to change or 0 to submit changes: ")
            for key, value in prod_fields.items():
                print(key, ". " + value[0])
            field = int(input("Enter field number: "))
            if field == 0:
                break
            if field < 0 or field > len(prod_fields):
                print()
                print("Invalid input! Enter again.")
                continue
            prod[prod_fields[field]] = input("Enter new value for %s: " % prod_fields[field])

        return prod

    def update_product_menu(self):
        print()
        prod_id = input("Enter ID of product to be updated: ").lower()
        if prod_id == 'all':
            print()
            print("You can't update multiple products at once. Enter a single product ID.")
            return False
        if prod_id not in self.prod_ids:
            print("This product doesn't exist in the database")
            return False
        message, success_code, prods_data = self.retrieve_products(prod_id)
        if success_code != 1:
            print(message)
            return False
        print()
        print(str(len(prods_data)) + ' product(s) retrieved. Printing...')
        print()
        for prod in prods_data:
            prod_str = []
            for key, value in prod.items():
                prod_str.append(key + " = " + value)
            print(" | ".join(prod_str[1:]))

        old_prod_id = prod = prods_data.values()[0]['prod_id']
        prod = self.update_field_menu(prods_data.values()[0])

        response = requests.patch(self.url + 'product/' + old_prod_id, data=prod)
        success_code = response['success_code']

        if success_code == 1:
            print()
            print(" Product was updated")

    def execute_user_command(self, command):
        if command > 4:
            print("Not a valid command")
            print()
            flow = None
            return
        if command == 1:
            flow = self.create_product_menu()
        if command == 2:
            flow = self.view_product_menu()
        if command == 3:
            flow = self.update_product_menu()
        if command == 4:
            flow = self.delete_product_menu()
        # elif command == 2:
        #     flow = self.initiate_delete_product()
        # elif command == 3:
        #     flow = self.initiate_update_product()
        # elif command == 4:
        #     flow = self.initiate_view_product()

        if not flow:
            print()
            print("The requested operation could not be performed due to an error. Returning to main menu", '\n')

        return
#
#
# if __name__ == 'main':
#     app = InvCLI()
#     while (choice := app.display_main_menu()) > 0:
#         app.execute_user_command(choice)
#     print("".join(["A", "B"]))
#     print("".join(["X" for x in range(20)]))
#     print("Terminal shut down.")
#     print("".join(["X" for x in range(20)]))
# # print(uuid4(now))
