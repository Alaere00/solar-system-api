from app import db
from app.models.moon import Moon
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response, request

moon_bp = Blueprint("moons", __name__, url_prefix="/moons")

def validate_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    moon = cls.query.get(model_id)
    
    if not moon:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not found"}, 404))
    
    return moon

@moon_bp.route("", methods=["POST"])
def create_moons():
    request_body = request.get_json()
    
    moon = Moon.create_moon(request_body)
    db.session.add(moon)
    db.session.commit()

    return make_response(jsonify(f"Moon {moon.name} is created"), 201)

@moon_bp.route("", methods=["GET"])
def get_moons():

    moons = Moon.query.all()
    moon_list = [moon.to_json() for moon in moons]
    
    return jsonify(moon_list)

@moon_bp.route("/<moon_id>/planets", methods=["POST"])
def create_planet(moon_id):
    moon = validate_id(Moon, moon_id)
    request_body = request.get_json()
    new_planet = Planet.create_planet(request_body)
    new_planet.moon = moon

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} with {moon.name}", 201)

@moon_bp.route("/<moon_id>/planets", methods=["GET"])
def read_planets(moon_id):
    moon = validate_id(Moon, moon_id)

    planets_response = [planet.to_json() for planet in moon.planets]

    return jsonify(planets_response)


