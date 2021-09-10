import logging

from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm

from wtforms import SubmitField, StringField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from core.models.beer import Beer, BeerType, BEER_TYPE_MAPPING, BeerCategory, BEER_CATEGORY_MAPPING
from core.persist import beers_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

admin_beers_blueprint = Blueprint('admin/beers/', __name__, template_folder='client/')


class BeerForm(FlaskForm):
    name = StringField('Nom de la bière:', validators=[DataRequired()])
    description = TextAreaField('Description de la bière:', validators=[DataRequired()])
    price = FloatField('Prix de la bière (au litre) : ', validators=[DataRequired()])
    alcohol_percentage = FloatField("Volume d'alcool (en %)", validators=[DataRequired()])
    image = StringField("Lien de l'image de la bière")
    beer_type = SelectField("Type de la bière:", choices=[b_t.value for b_t in BeerType])
    beer_category = SelectField("Catégorie de la bière:", choices=[b_c.value for b_c in BeerCategory])
    submit = SubmitField('Enregister')


@admin_beers_blueprint.route('/', methods=['GET', 'POST'])
@auth_required
def beers():
    form = BeerForm()
    message = ""
    if request.method == 'POST' and form.is_submitted():
        try:
            name = form.name.data
            logger.warning(f'Inserting beer {name} in DB')
            description = form.description.data
            price = form.price.data
            alcohol_percentage = form.alcohol_percentage.data
            image = form.image.data
            beer_type = form.beer_type.data
            beer_category = form.beer_category.data
            beer = Beer(name=name, description=description,
                        price=price,
                        alcohol_percentage=alcohol_percentage,
                        image=image, beer_type=BEER_TYPE_MAPPING[beer_type],
                        category=BEER_CATEGORY_MAPPING[beer_category])
            res = beers_repository.create_one(beer)
            # setting up the values displayed in the web page
            block_title = 'Niquel Miguel'
            message = "C'est bon, on a bien inséré ton beer en base donnée sans le moindre souci"
        except Exception as err:
            logger.warning(f'Error when inserting the beer'
                           f'inserted_id : {res.inserted_id}, beer_id : {beer._id} \n'
                           f'Error: {err}')
            block_title = 'Ooops'
            message = f'Ouula oops, on a rencontré une petite erreur en insérant ton beer en base de données 😅'

        return render_template('landing_page.html', message=message, block_title=block_title)

    return render_template('beers.html', form=form, message=message)
