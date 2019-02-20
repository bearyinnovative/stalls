# -*- coding: utf-8 -*-

from datetime import datetime
import logging

from bearychat import openapi
from component import Form, Text, Input
from component import Select, Option, DateSelect, ChannelSelect
from component.action import PrimaryAction, DangerAction
from envcfg.raw import stalls as config
from flask import url_for
from flask_babel import gettext as _

from stalls.extensions import db
from stalls.modules.poll import message
from stalls.modules.poll import form
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
    return form.setup_option_count


def cancel(payload):
    return message.make_error(_("Cancel"))


def select_count_option(payload):
    data = payload.get('data')
    option_count = None
    try:
        option_count = int(data.get('option_count'))
    except ValueError:
        return message.make_error(_('Parameters Error'))

    form = Form()
    form.add_fields(Text(value=_('Your are creating a poll with '
                                 '%(count)d options',
                                 count=option_count)),
                    Input(label=_('Description'), name='description'),
                    Input(name='option_count',
                          hidden=True, default_value=option_count))

    for each in range(option_count):
        label = _("Option %(idx)d", idx=(each+1))
        name = "option_{}".format(each + 1)
        form.add_field(Input(name=name, label=label))

    form.add_fields(Select(name='is_anonymous', label=_('Public or Anonymous'),
                           options=[Option(text=_('Public'), value=False),
                                    Option(text=_('Anonymous'), value=True)]),
                    DateSelect(name='end_datetime', label=_('Expiration')),
                    ChannelSelect(name='channel', label=_('Target Channel')))

    form.add_actions(PrimaryAction(name='create-poll', text=_('Confirm')),
                     DangerAction(name='cancel-create-poll', text=_('Cancel')))

    return form.render()


def cancel_select_option_count(payload):
    return message.make_error(_(u"Cancel"))


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
        return message.make_error(_("Parameters Error"))

    options = []
    for idx in range(option_count):
        options.append(data['option_{}'.format(idx+1)])

    raw_end_datetime = data.get('end_datetime', None)
    if raw_end_datetime:
        end_datetime = datetime.fromtimestamp(int(raw_end_datetime))
        if end_datetime <= datetime.utcnow():
            return message.make_error(_("Invalid Expiration"))

    poll = Poll(
        hubot_token=hubot_token,
        team_id=team_id,
        user_id=user_id,
        description=data.get('description'),
        option_count=option_count,
        is_anonymous=data.get('is_anonymous'),
        end_datetime=end_datetime,
        message_key=message_key,
    )

    poll.options = options
    poll.members = filter(None, [data.get('member')])
    poll.channels = filter(None, [data.get('channel')])
    poll.save()

    notify_members(payload, poll)
    notify_channels(payload, poll)

    poll.state = Poll.STATE_SENT
    poll.save()

    for each in options:
        option = PollOption(label=each, poll_id=poll.id)
        option.save(_commit=False)
    db.session.commit()

    return message.make_error("OK")


create_handlers = {
    'create': setup_option_count,
    'cancel-create': cancel,
    'select-option-count': select_count_option,
    'cancel-select-option-count': cancel_select_option_count,
    'create-poll': create_poll,
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
    poll_option_id = data.get('poll_option')

    if poll_option_id is None:
        return message.make_error(_('Please Choose Your Option'))

    poll_option = PollOption.query.get(poll_option_id)

    if poll_option is None:
        return message.make_error(_('Invalid Option'))

    poll = Poll.query.get(poll_id)
    if (poll is None or poll.team_id != team_id):
        return message.make_error(_('Invalid Poll'))

    us = UserSelection.get_by_poll_id_and_user_id(poll_id, user_id)
    if us is not None:
        return message.make_error(_('You have voted'))

    us = UserSelection(
        poll_id=poll.id,
        team_id=team_id,
        user_id=user_id,
        option_id=poll_option.id
    )
    us.save()

    return message.make_error(_('Opeartion Success'))


vote_handlers = {
    'confirm-poll': confirm_poll,
}
