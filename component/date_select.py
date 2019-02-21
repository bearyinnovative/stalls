# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class DateSelect(Action):

    type_ = 'date-select'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.placeholder = kwargs.get('placeholder')

        self._required_props = ('name', )
        self._optional_props = ('label', 'placeholder')
