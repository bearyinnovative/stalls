# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Section
from component import Select, SelectOption
from component import PrimarySubmit, DangerSubmit


def build_option(num):
    return SelectOption(_(text='with %(num)d options', num=num), value=num)


def create_setup_option_form():
    form = Form()
    form.add_actions(
        Section(value=_('Your are creating a poll, '
                        'how many options do you want?')),

        Select(name='option_count', label=_('Option Count'),
               options=[build_option(n) for n in range(2, 9 + 1)]),

        PrimarySubmit(name='poll/select-option-count', text=_('Confirm')),

        DangerSubmit(name='poll/cancel-select-option-count', text=_('Cancel')),
    )
    return form.render()
