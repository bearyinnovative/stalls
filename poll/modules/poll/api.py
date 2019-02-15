# -*- coding: utf-8 -*-

from __future__ import absolute_import
from copy import deepcopy
import logging

from component import Form, Text
from envcfg.raw import applet_poll as config
from flask import request, url_for
import requests

from poll.blueprint import create_api_blueprint
from poll.modules.poll.message import start, make_error
from poll.modules.poll.model.poll import Poll
from poll.modules.poll.service import process_create, process_vote
from poll.utils.api import json_response


bp = create_api_blueprint('poll', __name__)


@bp.route('/bearychat/poll/bearychat', methods=['GET', 'POST'])
def handle_message():
    hubot_token = request.json['token']
    data = {
        "token": hubot_token,
        "vchannel_id": request.json['vchannel'],
        "text": ("欢迎使用会议小助手！我可以帮助你在 BearyChat "
                 "中处理会议、投票！"
                 "您可以直接新建投票、会议，或使用模板来适用更多场景！"),
        "form_url": url_for("poll.start_poll", _external=True),
    }
    url = "{}/{}".format(config.OPENAPI_BASE, "message.create")
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        return 'ok'
    return 'failed'


@bp.route('/bearychat/poll')
def start_poll():
    return json_response(start)


@bp.route('/bearychat/poll', methods=['POST'])
def handle_poll():
    args = request.args
    payload = deepcopy(request.json)
    payload.update(args.to_dict())
    response = process_create(payload)
    if response is None:
        logging.getLogger('poll').info('none respond')
        return json_response(make_error(u'操作失败'))
    return json_response(response)


@bp.route('/bearychat/poll.vote')
def get_poll():
    args = request.args
    message_key = args['message_key']
    poll = Poll.query.filter(message_key=message_key).first()
    if poll is None:
        return json_response(make_error(u'投票已失效'))

    form = Form()
    form.add_fields(
        Text(label=u'投票说明', value=poll.description),
        Select()
    )
