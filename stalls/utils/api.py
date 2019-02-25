# -*- coding: utf-8 -*-

import json

from flask import make_response, jsonify


def json_response(data):
    return jsonify(data)
