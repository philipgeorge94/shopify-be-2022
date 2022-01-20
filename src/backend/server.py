import json

from flask import Flask, Response, request, send_file
import pymongo
import argparse

from src.backend.backend_utils.constants import *
from src.backend.backend_utils.backend_utils import export_to_csv
from src.backend.controller.controller import InvController

parser = argparse.ArgumentParser(description="Run server for inventory management")
parser.add_argument('-p', '--password', metavar='', required=True, help="Enter password received in application attachment 'auth.pdf'")
parser.add_argument('-i', '--port', type=int, metavar='', default=8000,
                    help="Specify port for server to run. Default is 8000")
args = parser.parse_args()
app = Flask(__name__)

try:
    # mongo = pymongo.MongoClient(
    #     host="localhost",
    #     port=27017,
    #     serverSelectionTimeoutMS=1000
    # )
    validated = False
    if args.password is None:
        raise Exception("You haven't entered a password")
    mongo = pymongo.MongoClient(
        f"{MONGO_CLIENT_PREFIX}://{MONGO_CLIENT_USERNAME}:{args.password}@{MONGO_CLIENT_SUFFIX}")

    mongo.server_info()  # triggers exception if cannot connect to db
    db = mongo.inventory
    invController = InvController(db)
    validated = True
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

@app.route("/product/export", methods = ["GET"])
def download_product_csv():
    prods_data, _, _ = invController.retrieve_product_record('all')
    filename = export_to_csv(prods_data)
    return send_file(filename,
                     mimetype='text/csv',
                     download_name=filename,
                     as_attachment=True)
    # return Response(
    #     response=json.dumps({"current working directory": os.getcwd()}),
    #     # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
    #     status=200,
    #     mimetype='application/json'
    # )


#######################################
if __name__ == "__main__":
    if validated:
        # logging.info("Starting Server")
        app.run(port=args.port, debug=True)
    else:
        print("Could not connect to the database, therefore exiting application")
