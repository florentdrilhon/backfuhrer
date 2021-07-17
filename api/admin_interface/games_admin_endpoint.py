from flask import Blueprint, jsonify, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import Form, SubmitField, StringField
from wtforms.validators import DataRequired

admin_games_blueprint = Blueprint('admin/games/', __name__, template_folder='client/')


class GameForm(FlaskForm):
    name = StringField('Nom du jeu:', validators=[DataRequired()])
    submit = SubmitField('Envoyer')


@admin_games_blueprint.route('/', methods=['GET', 'POST'])
def games():
    form = GameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        message = "c'est bon mon Daniel"
        return redirect('../../admin')
    else:
        message = "c'est pas bon mon Daniel"
    return render_template('games.html', form=form, message=message)
