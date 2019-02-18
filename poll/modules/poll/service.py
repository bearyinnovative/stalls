# -*- coding: utf-8 -*-

from datetime import datetime
import logging

from bearychat import openapi
from component import Form, Text, Input
from component import Select, Option, DateSelect, ChannelSelect, MemberSelect
from component.action import PrimaryAction, DangerAction
from envcfg.raw import applet_poll as config
from flask import url_for

from poll.extensions import db
from poll.modules.poll import message
from poll.modules.poll import form
from poll.modules.poll.model.poll import Poll, PollOption


def process_create(payload):
    action = payload['action']
    func = create_handlers.get(action)
    if callable(func):
        return func(payload)
    else:
        logging.getLogger('poll').info("action {} not found".format(action))
        return None


def setup_option_count(payload):
    return form.setup_option_count


def cancel(payload):
    return message.make_error("取消")


def select_count_option(payload):
    data = payload.get('data')
    option_count = None
    try:
        option_count = int(data.get('option_count'))
    except ValueError:
        return message.make_error(u'参数错误')

    if not option_count:
        return message.make_error(u'`data` not supported')

    form = Form()
    form.add_fields(Text(value=u'你将创建 %s 个选项的投票' % option_count),
                    Input(label=u'投票说明', name='description'),
                    Input(name='option_count',
                          hidden=True, default_value=option_count))

    for each in range(option_count):
        label = "选项 {}".format(each + 1)
        name = "option_{}".format(each + 1)
        form.add_field(Input(name=name, label=label))

    form.add_fields(Select(name='is_anonymous', label='公开/匿名',
                           options=[Option(text='公开', value=False),
                                    Option(text='匿名', value=True)]),
                    DateSelect(name='end_datetime', label=u'投票截止时间'),
                    MemberSelect(name='member', label=u'参与投票的成员'),
                    ChannelSelect(name='channel', label=u'接收讨论组'))

    form.add_actions(PrimaryAction(name='create-poll', text=u'创建投票'),
                     DangerAction(name='cancel-create-poll', text=u'取消投票'))

    return form.render()


def cancel_select_option_count(payload):
    return message.make_error("取消")


def create_poll(payload):
    message_key = payload['message_key']
    data = payload['data']
    option_count = 0
    try:
        option_count = int(data.get('option_count'))
    except ValueError:
        return message.make_error("参数错误")

    options = []
    for idx in range(option_count):
        options.append(data['option_{}'.format(idx+1)])

    end_datetime = data.get('end_datetime', None)
    if end_datetime:
        end_datetime = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")

    if end_datetime <= datetime.utcnow():
        return message.make_error("结束时间不合法")

    poll = Poll(
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
            'form_url': url_for('poll.get_poll', poll_id=poll.id, _external=True)
        })


def notify_members(payload, poll):
    pass


def process_vote(payload):
    action = payload['action']
    func = vote_handlers.get(action)
    if callable(func):
        return func(payload)
    else:
        logging.getLogger('poll').info("action {} not found".format(action))
        return None


vote_handlers = {}
