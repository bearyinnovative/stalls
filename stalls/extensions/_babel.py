# -*- coding: utf-8 -*-

from flask import request
from flask_babel import Babel

babel = Babel()


def setup_babel(app):
    babel.init_app(app)
    default = app.config.get('BABEL_DEFAULT_LOCALE', 'zh')
    supported = app.config.get('BABEL_SUPPORTED_LOCALES', ['zh', 'en'])

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(supported, default)
