# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class ChannelSelect(Action):

    type_ = 'channel-select'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.placeholder = kwargs.get('placeholder')
        self.multi = kwargs.get('multi')

        self._required_props = ('name', )
        self._optional_props = ('label', 'placeholder', 'multi')
