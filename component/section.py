# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class Section(Action):

    type_ = 'section'

    def __init__(self, **kwargs):
        value = kwargs.get('value', '')
        is_markdown = kwargs.get('is_markdown', True)

        self.text = {
            'value': value,
            'markdown': is_markdown,
        }

        self._required_props = ('text', )
        self._optional_props = []
