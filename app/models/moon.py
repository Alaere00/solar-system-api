from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)
    planets = db.relationship("Planet", back_populates="moon")

    @classmethod
    def create_moon(cls, moon_data):
        return cls(name=moon_data["name"])
    
    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }