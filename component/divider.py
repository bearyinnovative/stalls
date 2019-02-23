# -*- coding: utf-8 -*-

from component.base import Action


class Divider(Action):

    type_ = 'divider'

    def __init__(self):
        self._required_props = []
        self._optional_props = []
