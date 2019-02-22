# -*- coding: utf-8 -*-

from component import Form, Section, Submit


def make_msg(msg, submit=None):
    form = Form()
    form.add_action(Section(value=msg))
    if submit:
        form.add_action(Submit(**submit))
    return form.render()
