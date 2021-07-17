from flask import Blueprint, jsonify, redirect, render_template
from wtforms import Form, SubmitField

admin_games_blueprint = Blueprint('admin/games/', __name__, template_folder='client/')


@admin_games_blueprint.route('/', methods=['GET'])
def games():
    res = {'status': 'c niquel'}
    return jsonify(res)
