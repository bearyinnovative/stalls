# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class Checkbox(Action):

    type_ = 'checkbox'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.elements = []

        self._required_props = ('name', 'elements')
        self._optional_props = ('label', )

    def append(self, name, text):
        self.elements.append({'name': name, 'text': text})
