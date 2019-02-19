# -*- coding: utf-8 -*-

from __future__ import absolute_import
from copy import deepcopy
from datetime import datetime
import logging

from flask import abort, request, url_for

from poll.blueprint import create_api_blueprint
from poll.modules.poll.form import create_show_poll_form
from poll.modules.poll.form import (create_ready_show_poll_result_form,
                                    create_show_created_poll_result_form,
                                    create_show_joined_poll_result_form)
from poll.modules.poll.message import start, make_error
from poll.modules.poll.model.poll import Poll, UserSelection
from poll.modules.poll.service import process_create, process_vote
from poll.modules.poll.utils import (create_result_chart,
                                     get_p2p_vchannel_id,
                                     send_message_to_bearychat)
from poll.utils.api import json_response


bp = create_api_blueprint('poll', __name__)


@bp.route('/bearychat/poll/bearychat', methods=['GET', 'POST'])
def handle_message():
    token = request.json['token']
    if request.json['text'] in (u'投票结果', 'result'):
        data = {
            'text': '投票结果',
            "vchannel_id": request.json['vchannel'],
            "form_url": url_for("poll.show_poll_result", _external=True),
        }
    else:
        data = {
            "vchannel_id": request.json['vchannel'],
            "text": ("欢迎使用会议小助手！我可以帮助你在 BearyChat "
                     "中处理会议、投票！"
                     "您可以直接新建投票、会议，或使用模板来适用更多场景！"),
            "form_url": url_for("poll.start_poll", _external=True),
        }

    resp = send_message_to_bearychat(token, data)
    if 'error' in resp:
        return 'failed'
    return 'ok'


@bp.route('/poll.preview')
def preview_poll():
    poll_id = request.args.get('poll_id')
    visit_key = request.args.get('token')
    poll = Poll.get_by_id_and_visit_key(poll_id, visit_key)
    if poll is None:
        return abort(404)
    chart = create_result_chart(poll)
    return chart.render_response()


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
    id_ = args['poll_id']
    user_id = args['user_id']
    poll = Poll.query.get(id_)
    if poll is None:
        return json_response(make_error(u'投票已失效'))

    if datetime.utcnow() > poll.end_datetime:
        return json_response(make_error(u'投票已过期'))

    us = UserSelection.get_by_poll_id_and_user_id(poll.id, user_id)
    if us:
        return json_response(make_error(u'您已投票'))

    response = create_show_poll_form(poll)

    return json_response(response)


@bp.route('/bearychat/poll.vote', methods=['POST'])
def do_poll():
    args = request.args
    id_ = args['poll_id']
    poll = Poll.query.get(id_)
    if poll is None:
        return json_response(make_error(u'投票已失效'))

    if datetime.utcnow() > poll.end_datetime:
        return json_response(make_error(u'投票已过期'))

    payload = deepcopy(request.json)
    payload.update(args.to_dict())

    response = process_vote(payload)
    if response is None:
        logging.getLogger('poll').info('none respond')
        return json_response(make_error(u'操作失败'))
    return json_response(response)


@bp.route('/bearychat/poll.result')
def get_poll_result():
    args = request.args
    user_id = args['user_id']
    return json_response(create_ready_show_poll_result_form(user_id))


@bp.route('/bearychat/poll.result', methods=['POST'])
def show_poll_result():
    args = request.args
    payload = deepcopy(request.json)
    payload.update(args.to_dict())
    user_id = args['user_id']

    if payload['action'] == 'show-created-poll-result':
        form = create_show_created_poll_result_form(user_id)
        return json_response(form)

    if payload['action'] == 'show-joined-poll-result':
        form = create_show_joined_poll_result_form(user_id)
        return json_response(form)

    if payload['action'] == 'show-poll-result':
        data = payload['data']
        poll_id = data.get('poll_id')
        poll = Poll.query.get(poll_id)
        if poll:
            token = payload['token']
            vchannel_id = get_p2p_vchannel_id(token, user_id)
            image_url = url_for('poll.preview_poll',
                                poll_id=poll.id,
                                token=poll.visit_key,
                                _external=True)
            data = {
                'token': token,
                'vchannel_id': vchannel_id,
                'text': u'[投票 "{}" 的结果]({})'.format(
                    poll.description, image_url),
                'attachments': [
                    {
                        'images': [
                            {
                                'url': image_url,
                                'width': 800,
                                'height': 600,
                            }
                        ],
                    }
                ]
            }
            resp = send_message_to_bearychat(token, data)
            if 'error' in resp:
                return json_response(make_error(u'操作失败'))
        else:
            return json_response(make_error(u'操作失败'))

        return json_response(make_error(u'成功'))

    return json_response(make_error(u'操作失败'))
