# -*- coding: utf-8 -*-


class Action(object):

    kind = 'normal'

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.text = kwargs.get('text')
        self.confirm = kwargs.get('confirm')

    def render(self):
        rv = {
            'kind': self.kind,
            'name': self.name,
            'text': self.text
        }

        if self.confirm is not None:
            rv['confirm'] = self.confirm

        return rv


class PrimaryAction(Action):
    kind = 'primary'


class DangerAction(Action):
    kind = 'danger'
