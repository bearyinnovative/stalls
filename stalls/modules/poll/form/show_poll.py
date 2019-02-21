# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Section
from component import Select, SelectOption
from component import PrimarySubmit

from stalls.modules.poll.model.poll import PollOption


def create_show_poll_form(poll):
    poll_options = PollOption.get_multi_by_poll_id(poll.id)

    options = [SelectOption(text=each.label, value=each.id)
               for each in poll_options]

    form = Form()
    form.add_actions(
        Section(label=_('Description'), value=poll.description),

        Select(name="poll_option", options=options),

        PrimarySubmit(name='poll/confirm-poll', text=_('Confirm')),
    )
    return form.render()
