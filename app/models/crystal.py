from app import db 

class Crystal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    color = db.Column(db.String)
    powers = db.Column(db.String)

    # does not need decorator because we are passing an object into it
    def to_dict(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "color" : self.color,
            "powers" : self.powers
        }

    # need decorator because we are using it BEFORE we are creating an object
    @classmethod
    def from_dict(cls, crystal_data):
        # can also use cls below in place of Crystal
        new_crystal = Crystal(
            name = crystal_data["name"],
            color=crystal_data["color"],
            powers=crystal_data["powers"]
        )

        return new_crystal
