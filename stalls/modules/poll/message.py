# -*- coding: utf-8 -*-

from flask_babel import gettext as _

def get_start():
    return {
        "version": "1.0",
        "actions": [
            {
                "name": "create",
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
