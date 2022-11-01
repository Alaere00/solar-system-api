from crypt import methods
from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

def validate_id(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"planet {planet_id} is invalid"}, 400))

    planet = Planet.query.get(planet_id)
    
    if not planet:
        abort(make_response({"message": f"planet {planet_id} is not found"}, 404))
    
    return planet

@planet_bp.route("", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    planet_list = [planet.to_json() for planet in planets]
    
    return jsonify(planet_list)

@planet_bp.route("", methods=["POST"])
def create_planets():
    request_body = request.get_json()
    new_planets = Planet(name=request_body["name"], description=request_body["description"], color=request_body["color"])
    db.session.add(new_planets)
    db.session.commit()

    return make_response(f"Planets {new_planets.name} is created", 201)

@planet_bp.route("/<id>", methods=["GET"])
def handle_planet(id):
    planet = validate_id(id)

    return jsonify(planet.to_json())

@planet_bp.route("/<id>", methods=["PUT"])
def update_planet(id):
    planet = validate_id(id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]

    db.session.commit()

    return make_response(f"Planet #{id} successfully updated")

@planet_bp.route("/<id>", methods=["DELETE"])
def delete_planet(id):
    planet = validate_id(id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{id} successfully deleted")