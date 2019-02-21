# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form
from component import Submit


def getting_start(*args, **kwargs):

    form = Form()
    form.add_actions(
        Submit(name='poll/setup-form', text=_('Create Poll')))

    return form.render()
