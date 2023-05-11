from flask import Blueprint, jsonify, abort, make_response, request
from app import db 
from app.models.crystal import Crystal


crystal_bp = Blueprint("crystals",__name__, url_prefix="/crystals")

@crystal_bp.route("", methods=["POST"])
# define a route for creating a crystal resource
def create_crystals():
    # intializes request body
    request_body = request.get_json()

    # creates an instance of Crystal model based on request body using from_dict method 
    new_crystal = Crystal.from_dict(request_body)

    # adds and commits crystal to database
    db.session.add(new_crystal)
    db.session.commit()

    # returns success message
    return make_response(jsonify((f"Crystal {new_crystal.name} has been born! Woot woot!")), 201)

@crystal_bp.route("",methods=["GET"])
# defines route for getting all crystal resources
def handle_crystals():
    color_query = request.args.get("color")
    powers_query = request.args.get("powers")

    if color_query:
        crystals = Crystal.query.filter_by(color=color_query)
    elif powers_query:
        crystals = Crystal.query.filter_by(powers=powers_query)
    else:
    
        # gets all crystals from database, this returns a JSON dictionary
        crystals = Crystal.query.all() 

    # create empty response
    crystal_response = []

    # append each crystal to response
    for crystal in crystals:
        crystal_response.append(crystal.to_dict())
    
    # returns JSON response with all crystal details
    return jsonify(crystal_response), 200

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except: 
        abort(make_response({"message":f"{model_id} is not valid type ({type(model_id)}) invalid. Please use integer"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} does not exist"}, 404))
    
    return model

@crystal_bp.route("/<crystal_id>",methods=["GET"])
def get_one_crystal(crystal_id):
    crystal = validate_model(Crystal,crystal_id)

    return crystal.to_dict(), 200

@crystal_bp.route("/<crystal_id>",methods=["PUT"])
def add_one_crystal(crystal_id):
    crystal = validate_model(Crystal, crystal_id)

    request_body = request.get_json()

    crystal.name = request_body["name"]
    crystal.color = request_body["color"]
    crystal.powers = request_body["powers"]

    db.session.commit()

    return make_response(jsonify(f"{crystal.name} successfully updated"))

@crystal_bp.route("/<crystal_id>",methods=["DELETE"])
def remove_one_crystal(crystal_id):
    crystal = validate_model(Crystal, crystal_id)

    db.session.delete(crystal)
    db.session.commit()

    return make_response(jsonify(f"{crystal.name} was successfully deleted"))

# def handle_crystals():
#     crystal_response = []
#     for crystal in crystals:
#         crystal_response.append({
#             "id" : crystal.id,
#             "name" : crystal.name,
#             "color" : crystal.color,
#             "powers" : crystal.powers
#         })
#     return jsonify(crystal_response)

#creates crystal class
# class Crystal:
#     def __init__(self, id, name, color, powers):
#         self.id = id
#         self.name = name
#         self.color = color
#         self.powers = powers

#creates 3 instances of crystal
# crystals = [
#     Crystal(1, "Amethyst", "Purple", "Infinite knowledge and wisdom"),
#     Crystal(2, "Tiger's Eye", "Golden", "Strength, Power, confidence, daring"),
#     Crystal(3, "Rose Quartz", "Pink", "Find your one true love")
# ]

#responsible for validating and returning crystal instance 
# def validate_crystal(crystal_id):
    
#     try:
#         crystal_id = int(crystal_id)
#     except:
#         abort(make_response({"message":f"{crystal_id} not a valid integer"}, 400))

#     for crystal in crystals:
#         if crystal_id == crystal.id:
#             return crystal

#     abort(make_response({"message":f"crystal {crystal_id} does not exist"}, 404))

# crystal_bp = Blueprint("crystals",__name__, url_prefix="/crystals")

# @crystal_bp.route("", methods=["GET"])
# def handle_crystals():
#     crystal_response = []
#     for crystal in crystals:
#         crystal_response.append({
#             "id" : crystal.id,
#             "name" : crystal.name,
#             "color" : crystal.color,
#             "powers" : crystal.powers
#         })
#     return jsonify(crystal_response)

# # determine represenation and send back response
# @crystal_bp.route("/<crystal_id>", methods=["GET"])
# def handle_crystal(crystal_id):
#     crystal = validate_crystal(crystal_id)
    
#     return {
#         "id" : crystal.id,
#         "name" : crystal.name,
#         "color" : crystal.color,
#         "powers" : crystal.powers
#     }
    
