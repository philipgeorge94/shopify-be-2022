from src.backend.model.model import InvModel


class InvController:

    def __init__(self, db):
        self.model = InvModel(db)

    def create_product_record(self, prod_data):
        if (db_id := self.model.check_prod_id(prod_data["prod_id"])) != "":
            return db_id, 2, "Product already exists in database"
        else:
            db_id = self.model.add_product(prod_data)
            if db_id == '':
                return "", 0, "Product could not be inserted"
            else:
                return db_id, 1, "Product successfully inserted"

    def delete_product_record(self, prod_id):
        if (db_id := self.model.check_prod_id(prod_id)) == "":
            return db_id, 2, "Product doesn't exist in database"
        else:
            db_id = self.model.remove_product(prod_id)
            if db_id == '':
                return "", 0, "Product could not be deleted"
            else:
                return db_id, 1, "Product successfully deleted"
