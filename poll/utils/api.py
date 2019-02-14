# -*- coding: utf-8 -*-

import json


def json_response(data):
    return json.dumps(data), {"Content-Type": "application/json;charset=utf-8"}
