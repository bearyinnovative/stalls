# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Field, FieldError    # noqa


class Select(Field):

    type_ = 'select'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.label = kwargs.get('label')
        self.required = kwargs.get('required')

        self._props = {}
        self._props['defaultValue'] = kwargs.get('default_value')
        self._props['hidden'] = kwargs.get('hidden')
        self._props['disabled'] = kwargs.get('disabled')
        self._props['placeholder'] = kwargs.get('placeholder')
        self._props['description'] = kwargs.get('description')

        option_url = kwargs.get('option_url')
        if option_url:
            self._props['option_url'] = kwargs.get('option_url')
        else:
            options = kwargs.get('options', [])
            self._props['options'] = map(lambda x: x.render(), options)
