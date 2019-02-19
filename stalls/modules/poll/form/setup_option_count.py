# -*- coding: utf-8 -*-

from component import Form, Text
from component import Select, Option
from component.action import PrimaryAction, DangerAction


def create_form():
    form = Form()
    form.add_fields(Text(value=u'正在创建投票，请选择选项数量'),
                    Select(name='option_count',
                           label=u'选项数量',
                           options=[Option(text=u'2 个', value=2),
                                    Option(text=u'3 个', value=3),
                                    Option(text=u'4 个', value=4),
                                    Option(text=u'5 个', value=5),
                                    Option(text=u'6 个', value=6),
                                    Option(text=u'7 个', value=7),
                                    Option(text=u'7 个', value=8),
                                    Option(text=u'9 个', value=9)]))
    form.add_actions(
        PrimaryAction(name='select-option-count', text=u'确定'),
        DangerAction(name='cancel-select-option-count', text=u'取消'),
    )
    return form.render()


data = create_form()


del create_form
