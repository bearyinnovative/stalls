# -*- coding: utf-8 -*-

from flask_babel import gettext as _


def getting_start(*args, **kwargs):
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
