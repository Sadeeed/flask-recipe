from database import db

ingredients = db.Table('ingredients',
                       db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
                       db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
                       )


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    slug = db.Column(db.String(256))
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery',
                                  backref=db.backref('recipes', lazy=True))
    method = db.Column(db.String(10000))

    def __repr__(self):
        return f"<Recipe {self.name}>"

    def json(self):
        return {"id": self.id, "name": self.name, "slug": self.slug,
                "ingredients": list(x.json() for x in self.ingredients),
                "method": self.method}


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return f"<Ingredient {self.name}>"

    def json(self):
        return {"id": self.id, "name": self.name, "quantity": self.quantity}
