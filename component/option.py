# -*- coding: utf-8 -*-

from __future__ import absolute_import

from component.base import Field, FieldError    # noqa


class Option(object):

    def __init__(self, **kwargs):
        self.props = {}
        for f in ('text', 'value', 'img'):
            if f in kwargs:
                self.props[f] = kwargs.get(f)

    def validate(self):
        return True

    def render(self):
        self.validate()

        return self.props
