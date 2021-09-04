import logging

from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from core.models.game import GAME_NAMES_TYPES, Game, GAME_TYPES_NAMES
from core.persist import games_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

admin_games_blueprint = Blueprint('admin/games/', __name__, template_folder='client/')


class GameForm(FlaskForm):
    name = StringField('Nom du jeu:', validators=[DataRequired()])
    description = TextAreaField('Description du jeu:', validators=[DataRequired()])
    rules = TextAreaField('Règles du jeu:', validators=[DataRequired()])
    duration_min = IntegerField('Estimation de la durée du jeu (minutes):', validators=[DataRequired()])
    min_number_of_players = IntegerField('Nombre minimum de joueurs', validators=[DataRequired()])
    max_number_of_players = IntegerField('Nombre maximum de joueurs', validators=[DataRequired()])
    image = StringField("Lien de l'image du jeu")
    game_type = SelectField("Type du jeu:", choices=GAME_TYPES_NAMES.values())
    submit = SubmitField('Enregister')


@admin_games_blueprint.route('/', methods=['GET', 'POST'])
@auth_required
def games():
    form = GameForm()
    message = ""
    if form.validate_on_submit():
        name = form.name.data
        logger.warning(f'Inserting game {name} in DB')
        description = form.description.data
        rules = form.rules.data
        duration_min = form.duration_min.data
        min_number_of_players = form.min_number_of_players.data
        max_number_of_players = form.max_number_of_players.data
        image = form.image.data
        game_type = form.game_type.data
        if min_number_of_players > max_number_of_players:
            block_title = 'Ooops'
            message = "Erreur en insérant le jeu en base de données : \n" \
                      "Nombre minimum de joueur doit être inférieur au nombre maximum"
        else:
            try:
                game = Game(name=name, description=description, rules=rules, duration_min=duration_min,
                            number_of_players=(min_number_of_players, max_number_of_players),
                            image=image, game_type=GAME_NAMES_TYPES[game_type])

                res = games_repository.create_one(game)
                block_title = 'Niquel Miguel'
                message = "C'est bon, on a bien inséré ton jeu en base donnée sans le moindre souci"
            except Exception as err:
                logger.warning(f'Error when inserting the game'
                               f'inserted_id : {res.inserted_id}, game_id : {game._id} \n'
                               f'Error : {err}')
                block_title = 'Ooops'
                message = f'Ouula oops, on a rencontré une petite erreur en insérant ton jeu en base de données 😅'

        return render_template('landing_page.html', message=message, block_title=block_title)

    return render_template('games.html', form=form, message=message)
