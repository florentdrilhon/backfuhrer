from flask import Blueprint, jsonify, redirect, render_template
from wtforms import Form, SubmitField

admin_cocktails_blueprint = Blueprint('admin/cocktails/', __name__, template_folder='client/')


@admin_cocktails_blueprint.route('/', methods=['GET'])
def cocktails():
    res = {'status': 'c niquel'}
    return jsonify(res)
