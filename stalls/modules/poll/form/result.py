# -*- coding: utf-8 -*-

from flask import url_for
from flask_babel import gettext as _

from component import (Form, Section, Context, Input,
                       Select, SelectOption, Image,
                       Submit, PrimarySubmit)

from stalls.modules.poll.model import submit
from stalls.modules.poll.model.poll import Poll, UserSelection, PollOption


def show_poll(poll):
    poll_options = PollOption.get_multi_by_poll_id(poll.id)

    options = [SelectOption(text=each.label, value=each.id)
               for each in poll_options]

    form = Form()
    form.add_actions(
        Section(label=_('Description'), value=poll.description),

        Section(label=_('Poll Expiration'),
                value=poll.end_datetime.strftime("%Y-%m-%d %H:%M:%S")),

        Select(name="poll_option", options=options),

        PrimarySubmit(name=submit.CONFIRM_POLL, text=_('Confirm')),
    )
    return form.render()


def make_ready_form(user_id):
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


def show_created_polls(user_id):
    polls = Poll.get_multi_by_user_id(user_id)
    options = [SelectOption(text=each.description, value=each.id)
               for each in polls]
    form = Form()
    form.add_actions(
        Select(label=_('Polls I Created'), required=True, name='poll_id',
               options=options),

        Submit(name=submit.SHOW_RESULT, text=_('View Result')))
    return form.render()


def show_joined_polls(user_id):
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


def show_poll_result(poll):
    form = Form()
    context = Context()
    context.append('Poll Created')

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
