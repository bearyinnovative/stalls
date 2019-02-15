# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Field, FieldError    # noqa


class CheckboxGroup(Field):

    type_ = 'checkbox-group'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.required = kwargs.get('required')

        self._props = {}
        self._props['options'] = map(lambda x: x.redner,
                                     kwargs.get('options', []))
