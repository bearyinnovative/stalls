# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Section, Submit

from stalls.modules.poll.model import submit


def make_start_form(visit_key):
    form = Form()
    form.add_actions(
        Section(value=_('Create poll by clicking following button')),
        Submit(name=submit.SETUP_FORM, text=_('Create Poll')))

    return form.render()
