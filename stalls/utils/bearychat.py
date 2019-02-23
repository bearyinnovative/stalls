# -*- coding: utf-8 -*-

from bearychat import openapi
from envcfg.raw import stalls as config


def get_p2p_vchannel_id(token, user_id):
    client = openapi.Client(token, base_url=config.OPENAPI_BASE)
    c = client.p2p.create({'user_id': user_id})
    vchannel_id = c['vchannel_id']
    return vchannel_id


def send_message_to_bearychat(token, data):
    client = openapi.Client(token, base_url=config.OPENAPI_BASE)
    return client.message.create(json=data)
