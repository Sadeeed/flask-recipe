from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import login_required, current_user
from flask_restful import Resource
from slugify import slugify
from database import db

from apps.main.models import Recipe, Ingredient

main = Blueprint('main', __name__, template_folder="templates/main")


@main.route("/")
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)


@main.route("/recipe/<slug>")
def recipe(slug):
    recipe = Recipe.query.filter_by(slug=slug).first()
    if recipe:
        ingredients = recipe.ingredients
        method = recipe.method
        name = recipe.name
        return render_template('recipe.html', name=name, ingredients=ingredients,
                               method=method, id=recipe.id, vegan=recipe.vegan)
    else:
        flash("This recipe does not exist")
        return redirect(url_for('main.index'))


@main.route("/recipe/add", methods=['GET', 'POST'])
@login_required
def add_recipe():
    if request.method == 'GET':
        return render_template('add_recipe.html')

    if request.method == 'POST':
        mutable_request = request.form.copy()
        mutable_request.pop('name')
        mutable_request.pop('method')
        mutable_request.pop('vegan')

        new_recipe = Recipe(name=request.form['name'], slug=slugify(request.form['name']),
                            method=request.form['method'], vegan=True if request.form['vegan'] == 'true' else False)

        for ingredient in mutable_request.values():
            ingredient = Ingredient(name=ingredient)
            new_recipe.ingredients.append(ingredient)

        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('main.index'))


@main.route("/recipe/delete/<recipe_id>")
@login_required
def del_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
    else:
        flash("This recipe does not exist")
    return redirect(url_for('main.index'))


@main.route("/recipe/edit/<recipe_id>", methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if recipe:
        if request.method == 'GET':
            name = recipe.name
            ingredients = recipe.ingredients
            method = recipe.method
            vegan = recipe.vegan
            return render_template('edit_recipe.html', name=name, ingredients=ingredients, method=method, vegan=vegan)

        if request.method == 'POST':
            recipe.name = request.form['name']
            recipe.method = request.form['method']
            recipe.vegan = True if 'vegan' in request.form else False

            mutable_request = request.form.copy()
            mutable_request.pop('name')
            mutable_request.pop('method')
            if 'vegan' in request.form:
                mutable_request.pop('vegan')

            for ingredient, new_ingredient in zip(recipe.ingredients, mutable_request.values()):
                ingredient.name = new_ingredient
            db.session.commit()

            return redirect(url_for('main.recipe', slug=recipe.slug))
    else:
        flash("This recipe does not exist")
        return redirect(url_for('main.index'))


@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.app_errorhandler(404)
def page_not_found():
    return render_template('layouts/404.html'), 404


class RecipeList(Resource):
    def get(self):
        recipes = Recipe.query.all()
        return {'Recipes': list(x.json() for x in recipes)}

    def post(self):
        data = request.get_json()
        new_recipe = Recipe(name=data['name'], method=data['method'], slug=slugify(data['name']))
        for ingredient in data['ingredients']:
            ingredient = Ingredient(name=ingredient['name'])
            new_recipe.ingredients.append(ingredient)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe.json(), 201


class RecipeView(Resource):
    def get(self, recipe_id):
        recipe = Recipe.query.filter_by(id=recipe_id).first()
        if recipe:
            return recipe.json()
        else:
            return {'message': 'recipe not found'}, 404

    def put(self, recipe_id):
        data = request.get_json()

        recipe = Recipe.query.filter_by(id=recipe_id).first()

        if recipe:
            recipe.name = data['name']
            recipe.method = data['method']
        else:
            recipe = Recipe(name=data['name'], method=data['method'], slug=slugify(data['name']))

        db.session.add(recipe)
        db.session.commit()

        return recipe.json()
