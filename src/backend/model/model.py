from bson import ObjectId
from flask import Flask, Response, request
from bson.objectid import ObjectId
import json

from backend_utils.backend_utils import get_prod_id_list


class InvModel:
    def __init__(self, db):
        self.db = db

        # Initializing the list of prod_ids to enable easy checking of existing categories
        self.prod_categories = {
            "guitars": 13,
            "pianofortes": 17,
            "harmonicas": 10
        }

        # Initializing the list of prod_ids to enable easy checking of duplicates
        self.prod_ids = get_prod_id_list(self.get_prods('all'))

    def get_prod_categories(self):
        return self.prod_categories

    def get_prods(self, prod_id):
        try:
            if prod_id == 'all':
                data = list(self.db.product.find())
            else:
                data = list(self.db.product.find({"prod_id": prod_id}))

            for prod in data:
                prod["_id"] = str(prod["_id"])

            return data

        except Exception as ex:
            print(ex)
            return {}

    def check_prod_id(self, prod_id):
        if prod_id in self.prod_ids:
            return self.prod_ids[prod_id]
        return ""

    def add_prod_id(self, prod_id, db_id):
        print("in add_prod_id function")
        self.prod_ids[prod_id] = db_id

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
            }
            dbResponse = self.db.product.insert_one(query)
            print("dbResponse successful")

            # for attr in dir(dbResponse):
            #     print(attr);
            # print(dbResponse.inserted_id)
            self.add_prod_id(prod_data['prod_id'], dbResponse.inserted_id)

            return f"{dbResponse.inserted_id}"

        except Exception as ex:
            print(ex)
            return ""

    def remove_product(self, prod_id):
        print("in remove_product function")
        db_id = self.prod_ids[prod_id]
        try:
            query = {"_id": ObjectId(db_id)}
            dbResponse = self.db.product.delete_one(query)
            for attr in dir(dbResponse):
                print(f"****{attr}****")
            print("dbResponse successful")
            self.delete_prod_id(prod_id)
            return db_id

        except Exception as ex:
            print(ex)
            return ""
