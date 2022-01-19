import json
from flask import Flask, Response, request
import pymongo
from src.backend.controller.controller import InvController

app = Flask(__name__)

try:
    # mongo = pymongo.MongoClient(
    #     host="localhost",
    #     port=27017,
    #     serverSelectionTimeoutMS=1000
    # )
    mongo = pymongo.MongoClient("mongodb+srv://shopifybe2022_user:shopifybe2022_password@shopify-be-2022-db.fihoz.mongodb.net/shopify_inventory?retryWrites=true&w=majority")

    mongo.server_info()  # triggers exception if cannot connect to db
    db = mongo.inventory
    invController = InvController(db)
    pass

except Exception as ex:
    print(ex)
    pass


@app.route("/", methods=["GET"])
def affirm_connection():
    return Response(
        response=json.dumps({"message": "Connection established. Server running."}),
        status=200,
        mimetype='application/json'
    )


@app.route("/product", methods=["POST"])
def create_product():
    print("Request form: ", request.form)
    db_id, controller_response, message = invController.create_product_record(request.form)
    return Response(
        response=json.dumps(
            {"message": message,
             "id": db_id,
             "success_code": str(controller_response)
             },
        ),
        # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
        status=200 if controller_response > 0 else 422,
        mimetype='application/json'
    )


@app.route("/product/<prod_id>", methods=["DELETE"])
def delete_product(prod_id):
    db_id, controller_response, message = invController.delete_product_record(prod_id)
    return Response(
        response=json.dumps(
            {"message": message,
             "id": db_id,
             "success_code": str(controller_response)
             },
        ),
        # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
        status=200 if controller_response > 0 else 422,
        mimetype='application/json'
    )


@app.route("/product/<prod_id>", methods=["PATCH"])
def update_product(prod_id):
    db_id, controller_response, message = invController.update_product_record(prod_id, request.form)
    return Response(
        response=json.dumps(
            {"message": message,
             "id": db_id,
             "success_code": str(controller_response)
             },
        ),
        # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
        status=200 if controller_response > 0 else 422,
        mimetype='application/json'
    )


@app.route("/product/<prod_id>", methods=["GET"])
def retrieve_product(prod_id):
    prods_data, controller_response, message = invController.retrieve_product_record(prod_id)
    return Response(
        response=json.dumps(
            {"message": message,
             "success_code": str(controller_response),
             "prods_data": prods_data,
             },
        ),
        # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
        status=200 if controller_response > 0 else 422,
        mimetype='application/json'
    )


#######################################
if __name__ == "__main__":
    # logging.info("Starting Server")
    app.run(port=8000, debug=True)
