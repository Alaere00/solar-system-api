from crypt import methods
from flask import Blueprint, jsonify

class Planet:
    def __init__(self, id, name, description, color):
        self.id = id
        self.name = name
        self.description = description
        self.color = color

planets = [Planet(1, 'Mercury', 'closest to sun', 'gray'),
Planet(2, 'Mars', 'closest to Earth', 'red'),
Planet(3, 'Earth', 'our home', 'blue-green')]


planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planet_bp.route("", methods=["GET"])
def get_planets():
    planet = []
    for item in planets:
        planet.append({
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "color": item.color
        })

    return jsonify(planet)
    
