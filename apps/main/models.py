from database import db

ingredients = db.Table('ingredients',
                       db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
                       db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
                       )


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery',
                                  backref=db.backref('recipes', lazy=True))
    method = db.Column(db.String(150))

    def __repr__(self):
        return f"<Recipe {self.name}>"


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(256))
    quantity = db.column(db.Integer)

    def __repr__(self):
        return f"<Ingredient {self.name}>"
