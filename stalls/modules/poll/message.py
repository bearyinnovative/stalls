# -*- coding: utf-8 -*-

start = {
    "version": "1.0",
    "fields": [
        {
            "type": "text",
            "text": "投票"
        }
    ],
    "actions": [
        {
            "name": "create",
            "text": "新建投票",
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
