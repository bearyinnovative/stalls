# -*- coding: utf-8 -*-

from component import Form, Select, Option, Text
from component.action import Action

from poll.modules.poll.model.poll import Poll, UserSelection


def create_ready_show_poll_result_form(user_id):
    created_poll_count = Poll.count_by_user_id(user_id)
    joined_poll_count = UserSelection.count_by_user_id(user_id)

    form = Form()

    if created_poll_count + joined_poll_count == 0:
        form.add_field(Text(value="您还没参与投票"))

    if created_poll_count > 0:
        form.add_action(
            Action(name='show-created-poll-result', text='我创建的投票'))

    if joined_poll_count > 0:
        form.add_action(
            Action(name='show-joined-poll-result', text='我参与的投票'))

    return form.render()


def create_show_created_poll_result_form(user_id):
    polls = Poll.get_multi_by_user_id(user_id)
    options = [Option(text=each.description, value=each.id) for each in polls]
    form = Form()
    form.add_field(Select(label=u'选择创建的投票',
                          required=True,
                          name='poll_id',
                          options=options))
    form.add_action(Action(name='show-poll-result', text=u'查看结果'))
    return form.render()


def create_show_joined_poll_result_form(user_id):
    poll_ids = map(lambda x: x.id, UserSelection.get_multi_by_user_id(user_id))
    polls = Poll.get_multi_by_ids(poll_ids)
    options = [Option(text=each.description, value=each.id) for each in polls]
    form = Form()
    form.add_field(Select(label=u'选择参与的投票',
                          required=True,
                          name='poll_id',
                          options=options))
    form.add_action(Action(name='show-poll-result', text=u'查看结果'))
    return form.render()
