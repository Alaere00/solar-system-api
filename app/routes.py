from crypt import methods
from flask import Blueprint, jsonify, abort, make_response

class Planet:
    def __init__(self, id, name, description, color):
        self.id = id
        self.name = name
        self.description = description
        self.color = color

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color
        }

planets = [Planet(1, 'Mercury', 'closest to sun', 'gray'),
Planet(2, 'Mars', 'closest to Earth', 'red'),
Planet(3, 'Earth', 'our home', 'blue-green')]


planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planet_bp.route("", methods=["GET"])
def get_planets():
    planet = []
    for item in planets:
        planet.append(item.to_json())

    return jsonify(planet)

def validate_id(planet_id):
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message": f"planet {planet_id} is invalid"}, 400))

    for planet in planets:
        if planet_id == planet.id:
            return planet
    
    abort(make_response({"message": f"planet {planet_id} is not found"}, 404))

@planet_bp.route("/<id>", methods=["GET"])
def handle_planet(id):
    planet = validate_id(id)

    return jsonify(planet.to_json())
