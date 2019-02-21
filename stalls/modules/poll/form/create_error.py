# -*- coding: utf-8 -*-

from flask_babel import gettext as _

from component import Form, Section, Input
from component import Select, SelectOption
from component import ChannelSelect, MemberSelect, DateSelect
from component import PrimarySubmit, DangerSubmit


def create_error(msg):
    form = Form()
    form.add_action(Section(value=msg))
    return form.render()
