# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class Input(Action):

    type_ = 'input'

    def __init__(self, **kwargs):
        self._required_props = ('name')
        self._optional_props = ('label', 'value', 'hidden', 'placeholder')

        for f in self._required_props + self._optional_props:
            v = getattr(self, f)
            if v is not None:
                setattr(self, f, v)
