# -*- coding: utf-8 -*-

from __future__ import absolute_import
from copy import deepcopy
from datetime import datetime
import logging

from flask import abort, request, url_for
from flask_babel import gettext as _

from stalls.blueprint import create_api_blueprint
from stalls.modules.poll import form

from stalls.modules.poll.model import submit
from stalls.modules.poll.model.poll import Poll, UserSelection
from stalls.modules.poll.service import process_create, process_vote
from stalls.modules.poll.utils import (create_result_chart,
                                       send_message_to_bearychat)
from stalls.utils.api import json_response


bp = create_api_blueprint('poll', __name__)


@bp.route('/bearychat/poll/bearychat', methods=['GET', 'POST'])
def handle_message():
    token = request.json['token']
    if request.json['text'] in (u'投票结果', 'result'):
        data = {
            'text': _('Poll Result'),
            "vchannel_id": request.json['vchannel'],
            "form_url": url_for("poll.get_poll_result", _external=True),
        }
    else:
        data = {
            "vchannel_id": request.json['vchannel'],
            "text": ("欢迎使用会议小助手！我可以帮助你在 BearyChat "
                     "中处理投票~~、会议~~！"
                     "您可以直接新建投票~~、会议，或使用模板来适用更多场景~~！"),
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
    return json_response(form.make_start_form())


@bp.route('/bearychat/poll', methods=['POST'])
def handle_poll():
    args = request.args
    payload = deepcopy(request.json)
    payload.update(args.to_dict())
    response = process_create(payload)
    if response is None:
        logging.getLogger('poll').info('none respond')
        return json_response(form.make_msg(_('Operation Failed')))
    return json_response(response)


@bp.route('/bearychat/poll.vote')
def get_poll():
    args = request.args
    id_ = args['poll_id']
    user_id = args['user_id']
    poll = Poll.query.get(id_)
    if poll is None:
        return json_response(form.make_msg(_('Invalid Poll')))

    if datetime.utcnow() > poll.end_datetime:
        return json_response(form.make_msg(_('Poll Expired')))

    us = UserSelection.get_by_poll_id_and_user_id(poll.id, user_id)
    if us:
        response = form.show_poll_result(poll)
    else:
        response = form.show_poll(poll)

    return json_response(response)


@bp.route('/bearychat/poll.vote', methods=['POST'])
def do_poll():
    args = request.args
    id_ = args['poll_id']
    poll = Poll.query.get(id_)
    if poll is None:
        return json_response(form.make_msg(_('Invalid Poll')))

    if datetime.utcnow() > poll.end_datetime:
        return json_response(form.make_msg(_('Poll Expired')))

    payload = deepcopy(request.json)
    payload.update(args.to_dict())

    response = process_vote(payload)
    if response is None:
        logging.getLogger('poll').info('none respond')
        return json_response(form.make_msg(_('Operation Failed')))
    return json_response(response)


@bp.route('/bearychat/poll.result')
def get_poll_result():
    args = request.args
    user_id = args['user_id']
    return json_response(form.make_ready_form(user_id))


@bp.route('/bearychat/poll.result', methods=['POST'])
def show_poll_result():
    args = request.args
    payload = deepcopy(request.json)
    payload.update(args.to_dict())
    user_id = args['user_id']

    if payload['action'] == submit.SHOW_CREATED_RESULT:
        return json_response(
            form.show_created_polls(user_id))

    if payload['action'] == submit.SHOW_CREATED_RESULT:
        return json_response(form.show_joined_polls(user_id))

    if payload['action'] == submit.SHOW_RESULT:
        data = payload['data']
        poll_id = data.get('poll_id')
        poll = Poll.query.get(poll_id)
        if poll:
            return form.show_poll_result(poll)
        else:
            return json_response(form.make_msg(_('Operation Failed')))

    return json_response(form.make_msg(_('Operation Failed')))
