# -*- coding: utf-8 -*-

from flask_redis import FlaskRedis


redis = FlaskRedis()


def setup_redis(app):
    redis.init_app(app)
