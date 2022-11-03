from crypt import methods
from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

def validate_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    planet = cls.query.get(model_id)
    
    if not planet:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not found"}, 404))
    
    return planet

@planet_bp.route("", methods=["GET"])
def get_planets():
    name_query = request.args.get("name")
    description_query = request.args.get("description")
    color_query = request.args.get("color")

    planet_query = Planet.query

    if name_query:
        planet_query = planet_query.filter_by(name=name_query)
    if description_query:
        planet_query = planet_query.filter_by(description=description_query)
    if color_query:
        planet_query = planet_query.filter_by(color=color_query)

    planets = planet_query.all()
    planet_list = [planet.to_json() for planet in planets]
    
    return jsonify(planet_list)

@planet_bp.route("", methods=["POST"])
def create_planets():
    request_body = request.get_json()
    
    planet = Planet.create_planet(request_body)
    db.session.add(planet)
    db.session.commit()

    return make_response(jsonify(f"Planet {planet.name} is created"), 201)

@planet_bp.route("/<id>", methods=["GET"])
def handle_planet(id):
    planet = validate_id(Planet, id)

    return jsonify(planet.to_json())

@planet_bp.route("/<id>", methods=["PUT"])
def update_planet(id):
    planet = validate_id(Planet, id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.color = request_body["color"]

    db.session.commit()

    return make_response(f"Planet #{id} successfully updated")

@planet_bp.route("/<id>", methods=["DELETE"])
def delete_planet(id):
    planet = validate_id(Planet, id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"Planet #{id} successfully deleted")