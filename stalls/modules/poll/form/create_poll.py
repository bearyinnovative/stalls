# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Section, Input
from component import Select, SelectOption
from component import ChannelSelect, MemberSelect, DateSelect
from component import PrimarySubmit, DangerSubmit


def create_poll_form(option_count):
    form = Form()
    form.add_actions(
        Section(value=_('Your are creating a poll with %(count)d options',
                        count=option_count)),

        Input(label=_('Description'), name='description'),

        Input(name='option_count', hidden=True))

    for each in range(option_count):
        label = _("Option %(idx)d", idx=(each+1))
        name = "option_{}".format(each + 1)
        form.add_actions(Input(name=name, label=label))

    form.add_actions(
        Select(name='is_anonymous', label=_('Public or Anonymous'),
               options=[SelectOption(text=_('Public'), value=False),
                        SelectOption(text=_('Anonymous'), value=True)]),

        DateSelect(name='end_datetime', label=_('Expiration')),

        ChannelSelect(name='channel', label=_('Target Channel'), multi=True),

        MemberSelect(name='member', label=_('Target Member'), multi=True),

        PrimarySubmit(name='poll/confirm-create', text=_('Confirm')),

        DangerSubmit(name='poll/cancel-create', text=_('Cancel')))

    return form.render()
