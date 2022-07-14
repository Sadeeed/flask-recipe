from flask import Blueprint, request, url_for, redirect, render_template, flash
from flask_login import login_required, current_user

main = Blueprint('main', __name__, template_folder="templates/main")


@main.route("/")
def index():
    return render_template('index.html')


@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.app_errorhandler(404)
def page_not_found():
    return render_template('layouts/404.html'), 404
