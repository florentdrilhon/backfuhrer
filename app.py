import logging

from flask import Flask
from flask import request, jsonify

from api_routes.cocktails_endpoint import cocktails_blueprint
from api_routes.games_endpoint import games_blueprint

logger = logging.getLogger(__name__)

app = Flask(__name__)


def register_routes(app: Flask = app):
    app.register_blueprint(games_blueprint, url_prefix='/games')
    app.register_blueprint(cocktails_blueprint, url_prefix='/cocktails')


@app.route('/', methods=['GET'])
def hello():
    res = {'status': "C'est ok mon Daniel"}
    return jsonify(res)


register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
