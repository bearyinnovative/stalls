# -*- coding: utf-8 -*-

from component import Form, Text
from component import Select, Option
from component.action import PrimaryAction, DangerAction

from poll.modules.poll.model.poll import PollOption


def create_show_poll_form(poll):
    poll_options = PollOption.get_multi_by_poll_id(poll.id)

    options = [Option(text=each.label, value=each.id)
               for each in poll_options]

    form = Form()
    form.add_fields(
        Text(label=u'投票说明', value=poll.description),
        Select(name="poll_option", options=options),
    )

    form.add_actions(
        PrimaryAction(name='confirm-poll', text=u'确定'),
    )
    return form.render()
