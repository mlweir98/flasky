from flask import Blueprint, jsonify, abort, make_response, request
from app import db 
from app.models.crystal import Crystal
from app.models.healer import Healer
from app.crystal_routes import validate_model

healers_bp = Blueprint("healers", __name__, url_prefix="/healers")

@healers_bp.route("", methods=["POST"])
def create_healer():
    request_body = request.get_json()

    new_healer = Healer(name=request_body["name"])

    db.session.add(new_healer)
    db.session.commit()

    return make_response(jsonify(f"Crystal {new_healer.name} has been created"))

@healers_bp.route("", methods=["GET"])
def get_healers():
    healers = Healer.query.all()

    healers_response = []

    for healer in healers:
        healers_response.append(
            {
                "name": healer.name,
                "id" : healer.id
            }
        )
    
    return jsonify(healers_response)