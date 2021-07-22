from typing import Callable
from functools import wraps

from flask import request, make_response
from core.config import config
import logging

logger = logging.getLogger(__name__)


def auth_required(f: Callable):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == config.flask_admin.auth_username \
                and auth.password == config.flask_admin.auth_password:
            return f(*args, **kwargs)
        logger.warning(f'Username expected: {config.flask_admin.auth_username} \n'
                       f'Password expected: {config.flask_admin.auth_password}')
        return make_response("On a pas pu t'authentifier mon Daniel,"
                             " en plus t'as pas le passe sanitaire ça rentre même pas", 401,
                             {'WWW-Authenticate': 'Basic realm= "Login Required"'})

    return decorated
