# -*- coding: utf-8 -*-

import logging

from component import Form, Text, Input
from component import Select, Option, DateSelect, ChannelSelect, MemberSelect
from component.action import PrimaryAction, DangerAction

from poll.modules.poll import message
from poll.modules.poll import form
from poll.modules.poll.model.poll import Poll


def process(payload):
    action = payload['action']
    func = handlers.get(action)
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
                    MemberSelect(name='members', label=u'参与投票的成员'),
                    ChannelSelect(name='channels', label=u'接收讨论组'))

    form.add_actions(PrimaryAction(name='create-poll', text=u'创建投票'),
                     DangerAction(name='cancel-create-poll', text=u'取消投票'))

    return form.render()


def cancel_select_option_count(payload):
    return message.make_error("取消")


def create_poll(payload):
    data = payload['data']
    option_count = 0
    try:
        option_count = int(data.get('option_count')),
    except ValueError:
        return message.make_error("参数错误")

    options = []
    for idx in range(option_count):
        options.append(data['option_{}'.format(idx+1)])

    poll = Poll(
        description=data.get('description'),
        option_count=option_count,
        is_anonymous=data.get('description'),
        end_datetime=data.get('end_datetime'),
    )
    poll.options = options
    poll.members = data.get('members', [])
    poll.channels = data.get('channels', [])
    poll.save()
    return message.make_error("OK")


handlers = {
    'create': setup_option_count,
    'cancel-create': cancel,
    'select-option-count': select_count_option,
    'cancel-select-option-count': cancel_select_option_count,
    'create-poll': create_poll,
}
