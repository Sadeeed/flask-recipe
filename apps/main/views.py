from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import login_required, current_user
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
        return render_template('recipe.html', name=name, ingredients=ingredients, method=method, id=recipe.id)
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
        new_recipe = Recipe(name=request.form['name'], slug=slugify(request.form['name']),
                            method=request.form['method'])

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
            return render_template('edit_recipe.html', name=name, ingredients=ingredients, method=method)
        if request.method == 'POST':
            recipe.name = request.form['name']
            recipe.method = request.form['method']

            mutable_request = request.form.copy()
            mutable_request.pop('name')
            mutable_request.pop('method')

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
