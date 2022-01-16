import json
from flask import Flask, Response, request
import requests
import pymongo
from bson.objectid import ObjectId

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    mongo.server_info() #triggers exception if cannot connect to db
    db = mongo.company
    pass

except:
    pass

@app.route("/users", methods = ["GET"])
def get_some_users():
    try:
        data = list(db.users.find())
        for user in data:
            user["_id"] = str(user["_id"])

        return Response(
            response=json.dumps(data),
            # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
            status=200,
            mimetype='application/json'
        )

    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message": "cannot read user"}),
            # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
            status=500,
            mimetype='application/json'
        )

@app.route("/users", methods = ["POST"])
def create_user():
    try:
        user = {
            "firstName": request.form["firstName"],
            "lastName": request.form["lastName"]
        }
        dbResponse = db.users.insert_one(user)
        # for attr in dir(dbResponse):
        #     print(attr);
        print(dbResponse.inserted_id)
        return Response(
            response=json.dumps(
                {"message":"user created",
                 "id": f"{dbResponse.inserted_id}"
                },
            ),
            # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
            status = 200,
            mimetype = 'application/json'
        )

    except Exception as ex:
        print(ex)

@app.route("/users/<id>", methods = ["PATCH"])
def update_user(id):
    try:
        dbResponse = db.users.update_one(
            {"_id":ObjectId(id)},
            {"$set":{"firstName":request.form["firstName"]}}
        )
        # for attr in dir(dbResponse):
        #     print(f"*****{attr}*****")

        if dbResponse.modified_count > 0:
            return Response(
                response=json.dumps({"message": "user updated"}),
                # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps({"message": "nothing updated"}),
                # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
                status=200,
                mimetype='application/json'
            )

    except Exception as ex:
        print("*************")
        print(ex)
        print("*************")
        return Response(
            response=json.dumps({"message": "cannot update user"}),
            # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
            status=500,
            mimetype='application/json'
        )

@app.route("/users/<id>", methods=["DELETE"])
def delete_id(id):
    try:
        dbResponse = db.users.delete_one({"_id": ObjectId(id)})
        for attr in dir(dbResponse):
            print(f"*****{attr}*****")
        if dbResponse.deleted_count > 0:
            return Response(
                response=json.dumps({"message": f"user {id} deleted"}),
                # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
                status=200,
                mimetype='application/json'
            )
        else:
            return Response(
                response=json.dumps({"message": "nothing updated"}),
                # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
                status=200,
                mimetype='application/json'
            )

    except Exception as ex:
        print("*************")
        print(ex)
        print("*************")
        return Response(
            response=json.dumps({"message": "cannot delete user"}),
            # {"name":"Philip","ID":,f"{dbResponse.inserted_id}"},
            status=500,
            mimetype='application/json'
        )

#######################################
if __name__ == "__main__":
    # logging.info("Starting Server")
    app.run(port = 8000, debug=True)
#######################################






# """
# Flask server to handle requests from frontend
# Uses controller object
# """
# import logging
#
# from flask import Flask, request, render_template
# from flask_cors import CORS, cross_origin
#
# import json
# import webbrowser
#
# from src.backend.controller.controller import Controller
# from src.backend.model.model import Model
# from src.backend.utils import map_utils
#
# app = Flask(__name__)
#
# # For Cross Origin Resource sharing
# cors = CORS(app)
#
# # Instantiate controller
# ctr = Controller()
#
# # Define all routes
# @app.route('/', methods=['GET'])
# @cross_origin()
# def index():
#     return render_template("index.html", token="Hello SEleNa")
#
#
# @app.route('/route', methods=['POST'])
# @cross_origin()
# def route():
#
#     # Get input and decode values
#     data = json.loads(request.data)
#     print(data)
#
#     mode = data['mode']
#     algo = data['algorithm']
#     city = data['city']
#
#     # Load specified graph
#     map_file = "data/graph_" + city + ".pkl"
#     graph = map_utils.load_map(map_file)
#
#     limit = float(data['limit']) / 100
#
#     model = Model()
#     model.set_mode(mode)
#     model.set_limit(limit)
#     model.set_algorithm(algo)
#     model.set_source(data['start'])
#     model.set_destination(data['dest'])
#
#     ctr.set_model(model)
#
#     return ctr.handle_request(graph)
#
#
# if __name__ == "__main__":
#     logging.info("Starting Server")
#     app.run()
