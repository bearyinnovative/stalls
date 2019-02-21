# -*- coding: utf-8 -*-

from flask import url_for
from flask_babel import gettext as _

from component import (Form, Context, Section, Input,
                       Select, SelectOption, Image, Submit)

from stalls.modules.poll.model import submit
from stalls.modules.poll.model.poll import Poll, UserSelection, PollOption


def create_ready_show_poll_result_form(user_id):
    created_poll_count = Poll.count_by_user_id(user_id)
    joined_poll_count = UserSelection.count_by_user_id(user_id)

    form = Form()

    if created_poll_count + joined_poll_count == 0:
        form.add_action(Section(value=_("You have not joined any polls yet")))

    if created_poll_count > 0:
        form.add_action(
            Submit(name=submit.SHOW_CREATED_RESULT, text=_('Polls I Created')))

    if joined_poll_count > 0:
        form.add_action(
            Submit(name=submit.SHOW_CREATED_RESULT, text=_('Polls I Joined')))

    return form.render()


def create_show_created_poll_result_form(user_id):
    polls = Poll.get_multi_by_user_id(user_id)
    options = [SelectOption(text=each.description, value=each.id)
               for each in polls]
    form = Form()
    form.add_actions(
        Select(label=_('Polls I Created'), required=True, name='poll_id',
               options=options),

        Submit(name=submit.SHOW_RESULT, text=_('View Result')))
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
        Submit(name=submit.SHOW_RESULT, text=_('View Result')))
    return form.render()


def create_show_poll_result(poll):
    form = Form()
    context = Context()
    context.append(_('Poll Created'))

    form.add_actions(
        context,

        Input(value=poll.visit_key, name='token'),

        Section(value=_('Poll Name: %(description)s',
                        description=poll.description)),

        Section(value=_('Poll Expiration: %(expiration)s',
                expiration=poll.end_datetime.strftime("%Y-%m-%d %H:%M:%S"))),
    )

    poll_options = PollOption.get_multi_by_poll_id(poll.id)

    for idx, each in enumerate(poll_options):
        form.add_action(
            Section(value=u'{}. {}'.format(idx+1, each.label)))

    result_text = Context()
    result_text.append(_('Poll Result'))

    form.add_action(result_text)

    image_url = url_for('poll.preview_poll',
                        poll_id=poll.id,
                        token=poll.visit_key,
                        _external=True)

    form.add_actions(
        Image(title=_('Poll Result'), url=image_url),
        Submit(name=submit.REFRESH, label=_('Refresh')))

    return form.render()
