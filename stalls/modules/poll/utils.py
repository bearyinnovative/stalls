# -*- coding: utf-8 -*-

from base64 import b64encode
import pygal

from stalls.modules.poll.model.poll import PollOption, UserSelection


def create_result_chart(poll):
    options = (PollOption.get_multi_by_poll_id(poll.id, _execute=False)
                         .order_by(PollOption.id).all())
    chart = pygal.HorizontalBar(width=800, height=600, explicit_size=True)
    chart.title = poll.description
    for each in options:
        count_ = UserSelection.count_by_poll_id_and_option_id(poll.id, each.id)
        chart.add(each.label, count_)
    return chart


def svg2html_data(data):
    b = b64encode(data)
    return 'data:image/png;base64,{}'.format(b)
