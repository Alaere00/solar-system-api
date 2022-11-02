from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String, nullable = False)
    color = db.Column(db.String, nullable = False)

    @classmethod
    def create_planet(cls, planet_data):
        return cls(name=planet_data["name"],
                   description=planet_data["description"],
                   color=planet_data["color"])
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color
        }