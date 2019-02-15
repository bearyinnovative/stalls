# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .action import Action


VERSION = '1.0'


class Form(object):

    def __init__(self, fields=None, actions=None):
        self.fields = fields or []
        self.actions = actions or []

    def add_field(self, field):
        if isinstance(field, Field):
            self.fields.append(field)
        else:
            raise ValueError("`field` is not instance of Field")

    def add_fields(self, *fields):
        for field in fields:
            self.add_field(field)

    def add_action(self, action):
        if isinstance(action, Action):
            self.actions.append(action)
        else:
            raise ValueError("`action` is not instance of Action")

    def add_actions(self, *actions):
        for action in actions:
            self.add_action(action)

    @property
    def version(self):
        return VERSION

    def render(self):
        return {
            'version': self.version,
            'fields': map(lambda x: x.render(), self.fields),
            'actions': map(lambda x: x.render(), self.actions),
        }


class Field(object):

    @property
    def props(self):
        rt = {}
        for k, v in self._props.iteritems():
            if v is not None:
                rt[k] = v
        return rt

    def validate(self):
        return True

    def render(self):
        rv = {
            'type': self.type_,
            'name': self.name,
            'props': self.props,
        }

        label = getattr(self, 'label')
        if label is not None:
            rv['label'] = label

        required = getattr(self, 'required')
        if required is not None:
            rv['required'] = required

        return rv


class FieldError(Exception):
    pass
