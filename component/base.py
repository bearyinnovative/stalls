# -*- coding: utf-8 -*-


VERSION = '1.0'


class Form(object):

    def __init__(self, fields=None, actions=None):
        self.actions = actions or []

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
            'actions': map(lambda x: x.render(), self.actions),
        }


class Action(object):

    def __init__(self):
        self._required_props = []
        self._optional_props = []

    def validate(self):
        return True

    def render(self):
        rt = {'type': self.type_}

        for each in self._required_props:
            v = getattr(self, each)
            if v is not None:
                rt[each] = v

        for each in self._optional_props:
            v = getattr(self, each)
            if v is not None:
                rt[each] = v

        return rt
