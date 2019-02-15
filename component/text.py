# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Field, FieldError


class Text(Field):

    type_ = 'text'

    def __init__(self, **kwargs):
        self._props = {}
        self._props['value'] = kwargs.get('value')

    def validate(self):
        if self._props.get('value') is None:
            raise FieldError("`value` cannot be None")

    def render(self):
        self.validate()

        return {
            'type': self.type_,
            'props': self.props,
        }
