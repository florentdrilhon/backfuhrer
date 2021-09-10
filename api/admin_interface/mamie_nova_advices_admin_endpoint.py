import logging

from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm

from wtforms import SubmitField, StringField, SelectField, FormField, FieldList, TextAreaField
from wtforms.validators import DataRequired
from core.models.mamie_nova_advice import MamieNovaAdvice, MamieNovaAdviceType, MAMIE_NOVA_ADVICE_TYPE_MAPPING
from core.persist import mamie_nova_advices_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

admin_mamie_nova_advices_blueprint = Blueprint('admin/mamie_nova_advices/', __name__, template_folder='client/')


class LinkForm(FlaskForm):
    link_name = StringField('Nom du lien')
    link = StringField('Lien')


class MamieNovaAdviceForm(FlaskForm):
    name = StringField('Nom du conseil:', validators=[DataRequired()])
    description = TextAreaField('Description du conseil:', validators=[DataRequired()])
    links = FieldList(FormField(LinkForm), min_entries=4)
    image = StringField("Lien de l'image du mamie_nova_advice")
    mamie_nova_advice_type = SelectField("Type du conseil:", choices=[m_t.value for m_t in MamieNovaAdviceType])
    submit = SubmitField('Enregister')


@admin_mamie_nova_advices_blueprint.route('/', methods=['GET', 'POST'])
@auth_required
def mamie_nova_advices():
    form = MamieNovaAdviceForm()
    message = ""
    if request.method == 'POST' and form.is_submitted():
        try:
            name = form.name.data
            logger.warning(f'Trying to insert mamie_nova_advice {name} in DB')
            description = form.description.data
            links = {f['link_name']: f['link'] for f in form.links.data}
            image = form.image.data
            mamie_nova_advice_type = form.mamie_nova_advice_type.data
            mamie_nova_advice = MamieNovaAdvice(name=name, description=description,
                                                links=links,
                                                image=image,
                                                mamie_nova_advice_type=MAMIE_NOVA_ADVICE_TYPE_MAPPING[
                                                    mamie_nova_advice_type])
            res = mamie_nova_advices_repository.create_one(mamie_nova_advice)
            # setting up the values displayed in the web page
            block_title = 'Niquel Miguel' if res.inserted_id is not None else 'Ooops'
            message = "C'est bon, on a bien inséré ton conseil mamie nova en base donnée sans le moindre souci" \
                if res.inserted_id is not None \
                else f'Ouula oops, on a rencontré une petite erreur en insérant ton mamie_nova_advice en base de données 😅'
        except Exception as err:
            logger.warning(f'Error when inserting the mamie_nova_advice'
                           f'mamie_nova_advice_id : {mamie_nova_advice._id} \n'
                           f'Error: {err}')
            block_title = 'Ooops'
            message = f'Ouula oops, on a rencontré une petite erreur en insérant ton mamie_nova_advice en base de données 😅'

        return render_template('landing_page.html', message=message, block_title=block_title)

    return render_template('mamie_nova_advices.html', form=form, message=message)
