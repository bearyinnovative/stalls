# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class Image(Action):

    type_ = 'image'

    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.url = kwargs.get('url')

        self._required_props = ('title', 'url')
        self._optional_props = []
