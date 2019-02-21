# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class Select(Action):

    type_ = 'select'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.placeholder = kwargs.get('placeholder', '')
        self.multi = kwargs.get('multi', False)
        self.options = kwargs.options()

        self._required_props = ('name')
        self._optional_props = ('label', 'placeholder', 'multi', 'options')


class SelectOption(Action):

    def __init__(self, **kwargs):
        self.text = kwargs.get('text')
        self.value = kwargs.get('value')

        self._required_props = ('text', 'value')
        self._optional_props = []
