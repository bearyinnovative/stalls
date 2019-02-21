# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Section
from component import Select, SelectOption
from component import Submit

from stalls.modules.poll.model import submit


def build_option(num):
    return SelectOption(text=_('with %(num)d options', num=num), value=num)


def create_setup_option_form():
    form = Form()
    form.add_actions(
        Section(value=_('Your are creating a poll, '
                        'how many options do you want?')),

        Select(name='option_count', label=_('Option Count'),
               placeholder=_('Please select the number of options'),
               options=[build_option(n) for n in range(2, 9 + 1)]),

        Submit(name=submit.SELECT_OPTION_COUNT, text=_('Next')),
    )
    return form.render()
