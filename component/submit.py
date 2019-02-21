# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Action


class Submit(Action):

    type_ = 'submit'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.text = kwargs.get('text')
        self.kind = kwargs.get('kind')

        self._required_props = ('name', 'text')
        self._optional_props = ('kind', )


class PrimarySubmit(Action):

    type_ = 'submit'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.text = kwargs.get('text')
        self.kind = 'primary'

        self._required_props = ('name', 'text')
        self._optional_props = ('kind', )


class DangerSubmit(Action):

    type_ = 'submit'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.text = kwargs.get('text')
        self.kind = 'danger'

        self._required_props = ('name', 'text')
        self._optional_props = ('kind', )
