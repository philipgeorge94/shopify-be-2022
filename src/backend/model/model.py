from bson.objectid import ObjectId
from src.backend.backend_utils.backend_utils import get_prod_id_list


class InvModel:
    def __init__(self, db):
        self.prod_ids = None
        self.db = db

        # Initializing the list of prod_ids to enable easy checking of existing categories
        self.prod_categories = {
            "guitars": 13,
            "pianofortes": 17,
            "harmonicas": 10
        }
        self.refresh_prod_ids()

    def get_prod_categories(self):
        return self.prod_categories

    def check_prod_id(self, prod_id):
        if prod_id in self.prod_ids:
            return self.prod_ids[prod_id]
        return ""

    def refresh_prod_ids(self):
        print("in refresh_prod_ids function")
        all_prods, _ = self.get_product('all')
        self.prod_ids = get_prod_id_list(all_prods)

    def delete_prod_id(self, prod_id):
        del self.prod_ids[prod_id]

    def add_product(self, prod_data):
        print("in add_product function")
        try:
            query = {
                "prod_id": prod_data['prod_id'],
                "prod_name": prod_data['prod_name'],
                "prod_price": prod_data['prod_price'],
                "prod_desc": prod_data['prod_desc'],
                "prod_qty": prod_data['prod_qty'],
            }
            dbResponse = self.db.product.insert_one(query)
            print("dbResponse successful")

            # for attr in dir(dbResponse):
            #     print(attr);
            # print(dbResponse.inserted_id)
            self.refresh_prod_ids()

            return f"{dbResponse.inserted_id}"

        except Exception as ex:
            print(ex)
            return ""

    def remove_product(self, prod_id):
        print("in remove_product function")
        try:
            query = {"_id": ObjectId(self.prod_ids[prod_id])}
            dbResponse = self.db.product.delete_one(query)
            for attr in dir(dbResponse):
                print(f"****{attr}****")
            print("dbResponse successful")
            db_id = self.prod_ids[prod_id]
            self.refresh_prod_ids()
            return db_id

        except Exception as ex:
            print(ex)
            return ""

    def modify_product(self, prod_id, prod_data):
        print("in modify_product function")
        db_id = self.prod_ids[prod_id]
        try:
            queryFilter = {"_id": ObjectId(db_id)}
            queryValues = {
                "$set": {
                    "prod_id": prod_data['prod_id'],
                    "prod_name": prod_data['prod_name'],
                    "prod_price": prod_data['prod_price'],
                    "prod_desc": prod_data['prod_desc'],
                    "prod_qty": prod_data['prod_qty']
                }
            }
            dbResponse = self.db.product.update_one(queryFilter, queryValues)
            print("dbResponse successful")

            if dbResponse.modified_count > 0:
                self.refresh_prod_ids()
                return db_id, True
            else:
                return db_id, False

        except Exception as ex:
            print(ex)
            return "", False

    def get_product(self, prod_id):
        print("in get_product function")
        try:
            if prod_id == 'all':
                dbResponse = self.db.product.find()
            else:
                dbResponse = self.db.product.find({"prod_id": prod_id})

            prods_data = list(dbResponse)
            for prod in prods_data:
                prod["_id"] = str(prod["_id"])

            return prods_data, True

        except Exception as ex:
            print(ex)
            return {}, False
