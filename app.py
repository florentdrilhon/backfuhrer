import logging

from flask import Flask, render_template, request, make_response
from flask import jsonify, redirect
from flask_bootstrap import Bootstrap

from api.admin_interface.auth import auth_required
from api.routes.cocktails_endpoint import cocktails_blueprint
from api.routes.games_endpoint import games_blueprint
from api.admin_interface.games_admin_endpoint import admin_games_blueprint
from api.admin_interface.cocktails_admin_endpoint import admin_cocktails_blueprint
from core.config import config

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='api/admin_interface/client/')

app.config['SECRET_KEY'] = config.flask_admin.secret_key

Bootstrap(app)


def register_routes(app: Flask = app):
    app.register_blueprint(games_blueprint, url_prefix='/games')
    app.register_blueprint(cocktails_blueprint, url_prefix='/cocktails')
    app.register_blueprint(admin_games_blueprint, url_prefix='/admin/games')
    app.register_blueprint(admin_cocktails_blueprint, url_prefix='/admin/cocktails')


@app.route('/', methods=['GET'])
def hello():
    res = {'status': "C'est ok mon bon Daniel"}
    return jsonify(res)


@app.route('/admin/', methods=['GET', 'POST'])
@auth_required
def home():
    return render_template('index.html')


register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
