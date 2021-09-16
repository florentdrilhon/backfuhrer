import logging

from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm

from wtforms import SubmitField, StringField, IntegerField, SelectField, FormField, FieldList, TextAreaField
from wtforms.validators import DataRequired
from core.models.cocktail import Cocktail, CocktailType, COCKTAIL_TYPE_MAPPING
from core.persist import cocktails_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

admin_cocktails_blueprint = Blueprint('admin/cocktails/', __name__, template_folder='client/')


class IngredientForm(FlaskForm):
    ingredient_name = StringField('Ingrédient')
    quantity = StringField('Quantité et unité (ex: 5g)')


class CocktailForm(FlaskForm):
    name = StringField('Nom du cocktail:', validators=[DataRequired()])
    description = StringField('Courte description du cocktail:', validators=[DataRequired()])
    recipe = FieldList(StringField('Etape:'), min_entries=6)
    ingredients = FieldList(FormField(IngredientForm), min_entries=6)
    preparation_time_min = IntegerField('Estimation de la durée de préparation du cocktail (minutes):',
                                        validators=[DataRequired()])
    image = StringField("Lien de l'image du cocktail")
    cocktail_type = SelectField("Type du cocktail:", choices=[c_t.value for c_t in CocktailType])
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
            recipe = [d for d in form.recipe.data if len(d) > 0]
            ingredients = {f['ingredient_name']: f['quantity'] for f in form.ingredients.data}
            preparation_time_min = form.preparation_time_min.data
            image = form.image.data
            cocktail_type = form.cocktail_type.data
            cocktail = Cocktail(name=name, description=description,
                                recipe=recipe,
                                ingredients=ingredients,
                                preparation_time_min=preparation_time_min,
                                image=image, cocktail_type=COCKTAIL_TYPE_MAPPING[cocktail_type])
            res = cocktails_repository.create_one(cocktail)
            # setting up the values displayed in the web page
            block_title = 'Niquel Miguel'
            message = "C'est bon, on a bien inséré ton cocktail en base donnée sans le moindre souci"
        except Exception as err:
            logger.warning(f'Error when inserting the cocktail'
                           f'cocktail_id : {cocktail._id} \n'
                           f'Error: {err}')
            block_title = 'Ooops'
            message = f'Ouula oops, on a rencontré une petite erreur en insérant ton cocktail en base de données 😅'

        return render_template('landing_page.html', message=message, block_title=block_title)

    return render_template('cocktails.html', form=form, message=message)
