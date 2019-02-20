# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Text
from component import Select, Option
from component.action import PrimaryAction, DangerAction


def create_form():
    form = Form()
    form.add_fields(Text(value=_('Your are creating a poll, '
                                 'how many options do you want?')),
                    Select(name='option_count',
                           label=_('Option Count'),
                           options=[
                               Option(text=_('with %(num)d options', num=2),
                                      value=2),
                               Option(text=_('with %(num)d options', num=3),
                                      value=3),
                               Option(text=_('with %(num)d options', num=4),
                                      value=4),
                               Option(text=_('with %(num)d options', num=5),
                                      value=5),
                               Option(text=_('with %(num)d options', num=6),
                                      value=6),
                               Option(text=_('with %(num)d options', num=7),
                                      value=7),
                               Option(text=_('with %(num)d options', num=8),
                                      value=8),
                               Option(text=_('with %(num)d options', num=9),
                                      value=9),
                               ]))
    form.add_actions(
        PrimaryAction(name='select-option-count', text=_(u'Confirm')),
        DangerAction(name='cancel-select-option-count', text=_(u'Cancel')),
    )
    return form.render()


data = create_form()


del create_form
