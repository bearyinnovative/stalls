# -*- coding: utf-8 -*-

from flask_babel import gettext as _

def get_start(*args, **kwargs):
    return {
        "version": "1.0",
        "actions": [
            {
                "name": "poll/setup-form",
                "text": _('Create Poll'),
                "kind": "normal"
            }
        ],
    }


def make_error(msg):
    return {
        'version': '1.0',
        'fields': [
            {
                'type': 'text',
                'props': {
                    'value': msg,
                }
            }
        ]
    }
