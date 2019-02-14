# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import Blueprint, jsonify


def create_api_blueprint(name, package_name, **kwargs):
    """Create API blueprint for operating events

    :param name: The name of endpoint.
    :param package_name: Always be `__name__`.
    :param url_prefix: The url prefix of relative URL.
    """

    url_prefix = kwargs.pop('url_prefix', '')
    url_prefix = '/{url_prefix}{name}'.format(
        name=name, url_prefix=url_prefix)

    blueprint_name = '{name}'.format(name=name)
    return _create_bp(blueprint_name, package_name,
                      url_prefix=url_prefix, **kwargs)


def _create_bp(name, package_name, **kwargs):
    """Create blueprint"""

    url_prefix = kwargs.pop('url_prefix', '')

    bp = Blueprint(
        name, package_name,
        url_prefix=url_prefix,
        **kwargs)

    @bp.errorhandler(400)
    @bp.errorhandler(401)
    @bp.errorhandler(403)
    @bp.errorhandler(404)
    @bp.errorhandler(405)
    @bp.errorhandler(503)
    def handle_http_error(error):
        errors = [
            {'message': error.description,
             'kind': 'http_error_{http_code}'.format(http_code=error.code)}]
        return jsonify(success=False, errors=errors), error.code

    return bp
