# -*- coding: utf-8 -*-

from component.base import Action


class Context(Action):

    type_ = 'context'

    def __init__(self, **kwargs):
        self.elements = []
        self._required_props = ('elements', )
        self._optional_props = []

    def append(self, text, is_markdown=True):
        self.elements.append({
            'type': 'text',
            'text': text,
            'markdown': is_markdown,
        })
