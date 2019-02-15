# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Field, FieldError    # noqa


class Checkbox(Field):

    type_ = 'checkbox'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.required = kwargs.get('required')

        self._props = {}
        self._props['checked'] = kwargs.get('checked')
        self._props['name'] = kwargs.get('name')
        self._props['text'] = kwargs.get('text')
        self._props['disabled'] = kwargs.get('disabled')
