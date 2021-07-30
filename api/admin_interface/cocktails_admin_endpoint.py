import logging

from flask import Blueprint, redirect, render_template, request, url_for
from flask_wtf import FlaskForm

from wtforms import SubmitField, StringField, IntegerField, SelectField, FormField, FieldList, TextAreaField
from wtforms.validators import DataRequired
from core.models.cocktail import COCKTAIL_NAMES_TYPES, Cocktail, COCKTAIL_TYPES_NAMES
from core.persist import cocktails_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

admin_cocktails_blueprint = Blueprint('admin/cocktails/', __name__, template_folder='client/')


class IngredientForm(FlaskForm):
    ingredient_name = StringField('Ingrédient')
    quantity = StringField('Quantité et unité (ex: 5g)')


class CocktailForm(FlaskForm):
    name = StringField('Nom du cocktail:', validators=[DataRequired()])
    description = TextAreaField('Description du cocktail:', validators=[DataRequired()])
    ingredients = FieldList(FormField(IngredientForm), min_entries=6)
    preparation_time_min = IntegerField('Estimation de la durée de préparation du cocktail (minutes):',
                                        validators=[DataRequired()])
    image = StringField("Lien de l'image du cocktail")
    cocktail_type = SelectField("Type du cocktail:", choices=COCKTAIL_TYPES_NAMES.values())
    submit = SubmitField('Enregister')


@admin_cocktails_blueprint.route('/', methods=['GET', 'POST'])
@auth_required
def cocktails():
    form = CocktailForm()
    message = ""
    if request.method == 'POST' and form.is_submitted():
        try:
            name = form.name.data
            logger.warning(f'Inserting cocktail {name} in DB')
            description = form.description.data
            ingredients = {f['ingredient_name']: f['quantity'] for f in form.ingredients.data}
            preparation_time_min = form.preparation_time_min.data
            image = form.image.data
            cocktail_type = form.cocktail_type.data
            cocktail = Cocktail(name=name, description=description,
                                ingredients=ingredients,
                                preparation_time_min=preparation_time_min,
                                image=image, cocktail_type=COCKTAIL_NAMES_TYPES[cocktail_type])

            res = cocktails_repository.create_one(cocktail)
        except Exception as err:
            logger.warning(f'Error when inserting the cocktail'
                           f'inserted_id : {res.inserted_id}, cocktail_id : {cocktail._id} \n'
                           f'Error: {err}')
            return render_template('error.html', entity='cocktail')
        return redirect(url_for('home'))

    return render_template('cocktails.html', form=form, message=message)
