# -*- coding: utf-8 -*-

from component import Form, Section


def make_msg(msg):
    form = Form()
    form.add_action(Section(value=msg))
    return form.render()
