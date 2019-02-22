# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import (Form, Section, Input,
                       Select, SelectOption,
                       ChannelSelect, DateSelect,
                       Submit, PrimarySubmit)

from stalls.modules.poll.model import submit


def make_option_count_form():
    def build_option(num):
        return SelectOption(text=_('with %(num)d options', num=num),
                            value=str(num))

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


def make_poll_form(option_count):
    form = Form()
    form.add_actions(
        Section(value=_('Your are creating a poll with %(count)d options',
                        count=option_count)),

        Input(label=_('Poll Name'), name='description'),

        Input(name='option_count', hidden=True, value=option_count))

    for each in range(option_count):
        label = _("Option %(idx)d", idx=(each+1))
        name = "option_{}".format(each + 1)
        form.add_action(Input(name=name, label=label))

    form.add_actions(
        DateSelect(name='end_timestamp', label=_('Poll Expiration')),

        ChannelSelect(name='channels', label=_('Target Channel'), multi=True),

        PrimarySubmit(name=submit.CONFIRM_CREATE,
                      text=_('Create and Send Poll')),
    )

    return form.render()
