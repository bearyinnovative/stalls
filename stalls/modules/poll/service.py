# -*- coding: utf-8 -*-

from datetime import datetime
import logging

from bearychat import openapi
from envcfg.raw import stalls as config
from flask import url_for
from flask_babel import gettext as _

from stalls.extensions import db
from stalls.modules.poll import form
from stalls.modules.poll.model import submit
from stalls.modules.poll.model.poll import Poll, PollOption, UserSelection


def process_create(payload):
    action = payload['action']
    func = create_handlers.get(action)
    if callable(func):
        return func(payload)
    else:
        logging.getLogger('stalls').info("action {} not found".format(action))
        return None


def setup_option_count(payload):
    return form.make_option_count_form()


def select_count_option(payload):
    data = payload.get('data')
    option_count_arr = data.get('option_count', [])

    if (not isinstance(option_count_arr, list)) or len(option_count_arr) != 1:
        return form.make_msg(_('Parameters Error'))

    option_count = option_count_arr[0]
    try:
        option_count = int(option_count)
    except ValueError:
        return form.make_msg(_('Parameters Error'))

    return form.make_poll_form(option_count)


def create_poll(payload):
    hubot_token = payload['token']
    team_id = payload['team_id']
    user_id = payload['user_id']
    message_key = payload['message_key']
    data = payload['data']
    option_count = 0
    try:
        option_count = int(data.get('option_count'))
    except ValueError:
        return form.make_msg(_("Parameters Error"))

    options = []
    for idx in range(option_count):
        options.append(data['option_{}'.format(idx+1)])

    raw_end_timestamp = data.get('end_timestamp', 0)
    try:
        end_timestamp = int(raw_end_timestamp)
    except (ValueError, TypeError) as e:
        logging.getLogger('stalls').info(
            "end_timetamp {} error: {}".format(raw_end_timestamp,
                                               e.get_message()))
        return form.make_msg(_("Invalid Expiration"))

    end_datetime = datetime.fromtimestamp(end_timestamp)
    if end_datetime <= datetime.utcnow():
        return form.make_msg(_("Invalid Expiration"))

    poll = Poll(
        hubot_token=hubot_token,
        team_id=team_id,
        user_id=user_id,
        description=data.get('description'),
        option_count=option_count,
        is_anonymous=data.get('is_anonymous', False),
        end_datetime=end_datetime,
        message_key=message_key,
    )

    poll.options = options
    poll.members = filter(None, data.get('members', []))
    poll.channels = filter(None, data.get('channels', []))
    poll.save()

    notify_members(payload, poll)
    notify_channels(payload, poll)

    poll.state = Poll.STATE_SENT
    poll.save()

    for each in options:
        option = PollOption(label=each, poll_id=poll.id)
        option.save(_commit=False)

    db.session.commit()

    return form.show_poll_result(poll)


def refresh_poll(payload):
    data = payload['data']
    token = data.get('token')
    poll = Poll.get_by_visit_key(token)
    if poll:
        return form.show_poll_result(poll)
    return form.make_msg(_('Poll Not Found'))


create_handlers = {
    submit.SETUP_FORM: setup_option_count,
    submit.SELECT_OPTION_COUNT: select_count_option,
    submit.CONFIRM_CREATE: create_poll,
    submit.REFRESH: refresh_poll,
}


def notify_channels(payload, poll):
    token = payload.get('token')
    client = openapi.Client(token, base_url=config.OPENAPI_BASE)
    for each in poll.channels:
        c = client.channel.info({'channel_id': each})
        vchannel_id = c['vchannel_id']
        client.message.create({
            'vchannel_id': vchannel_id,
            'text': 'vote',
            'form_url': url_for('poll.get_poll',
                                poll_id=poll.id,
                                _external=True)
        })


def notify_members(payload, poll):
    token = payload.get('token')
    client = openapi.Client(token, base_url=config.OPENAPI_BASE)
    for each in poll.members:
        c = client.p2p.create({'user_id': each})
        vchannel_id = c['vchannel_id'],
        client.message.create({
            'vchannel_id': vchannel_id,
            'text': 'vote',
            'form_url': url_for('poll.get_poll',
                                poll_id=poll.id,
                                _external=True)
        })


def process_vote(payload):
    action = payload['action']
    func = vote_handlers.get(action)
    if callable(func):
        return func(payload)
    else:
        logging.getLogger('poll').info("action {} not found".format(action))
        return None


def confirm_poll(payload):
    poll_id = payload['poll_id']
    team_id = payload['team_id']
    user_id = payload['user_id']
    data = payload['data']
    poll_option_ids = data.get('poll_option', [])

    if len(poll_option_ids) != 1:
        return form.make_msg(_('Please Choose Your Option'))

    poll_option_id = poll_option_ids[0]

    poll_option = PollOption.query.get(poll_option_id)

    if poll_option is None:
        return form.make_msg(_('Invalid Option'))

    poll = Poll.query.get(poll_id)
    if (poll is None or poll.team_id != team_id):
        return form.make_msg(_('Invalid Poll'))

    us = UserSelection.get_by_poll_id_and_user_id(poll_id, user_id)
    if us is not None:
        return form.make_msg(_('You have voted'))

    us = UserSelection(
        poll_id=poll.id,
        team_id=team_id,
        user_id=user_id,
        option_id=poll_option.id
    )
    us.save()

    return form.make_msg(_('Opeartion Success'))


vote_handlers = {
    submit.CONFIRM_POLL: confirm_poll,
}
