# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Section, Select, SelectOption
from component import Submit

from stalls.modules.poll.model.poll import Poll, UserSelection


def create_ready_show_poll_result_form(user_id):
    created_poll_count = Poll.count_by_user_id(user_id)
    joined_poll_count = UserSelection.count_by_user_id(user_id)

    form = Form()

    if created_poll_count + joined_poll_count == 0:
        form.add_action(Section(value=_("You have not joined any polls yet")))

    if created_poll_count > 0:
        form.add_action(
            Submit(name='poll/show-created-result', text=_('Polls I Created')))

    if joined_poll_count > 0:
        form.add_action(
            Submit(name='poll/show-joined-result', text=_('Polls I Joined')))

    return form.render()


def create_show_created_poll_result_form(user_id):
    polls = Poll.get_multi_by_user_id(user_id)
    options = [SelectOption(text=each.description, value=each.id)
               for each in polls]
    form = Form()
    form.add_actions(
        Select(label=_('Polls I Created'), required=True, name='poll_id',
               options=options),

        Submit(name='poll/show-result', text=_('View Result')))
    return form.render()


def create_show_joined_poll_result_form(user_id):
    poll_ids = map(lambda x: x.id, UserSelection.get_multi_by_user_id(user_id))
    polls = Poll.get_multi_by_ids(poll_ids)
    options = [SelectOption(text=each.description, value=each.id)
               for each in polls]
    form = Form()
    form.add_actions(
        Select(label=_('Polls I Joined'), required=True, name='poll_id',
               options=options),
        Submit(name='poll/show-result', text=_('View Result')))
    return form.render()
