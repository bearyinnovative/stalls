# -*- coding: utf-8 -*-

from __future__ import absolute_import

from flask import request

from poll.blueprint import create_api_blueprint
from poll.modules.poll.message import start, error
from poll.modules.poll.service import process_data
from poll.utils.api import json_response


bp = create_api_blueprint('poll', __name__)


@bp.route('/bearychat/poll')
def get_poll():
    return json_response(start)


@bp.route('/bearychat/poll', methods=['POST'])
def handle_poll():
    print request.headers
    data = request.json
    response = process_data(data)
    if response is None:
        return json_response(error)
    return json_response(response)


@bp.route('/bearychat/poll/bearychat', methods=['GET', 'POST'])
def handle_message():
    hubot_token = request.json['token']
    data = {
        "token": hubot_token,
        "vchannel_id": request.json['vchannel'],
        "text": "欢迎使用会议小助手！我可以帮助你在 BearyChat 中处理会议、投票！您可以直接新建投票、会议，或使用模板来适用更多场景！",
        "form_url": url_for("vote_handler", _external=True),
    }
    resp = requests.post("{}/{}".format(api_base, "message.create"), json=data)
    return 'ok'
