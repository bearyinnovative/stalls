# -*- coding: utf-8 -*-

from flask import url_for
from flask_babel import gettext as _

from stalls.app import create_app
from stalls.modules.poll.model.poll import Poll
from stalls.utils.bearychat import (get_p2p_vchannel_id,
                                    send_message_to_bearychat)


EXPIRED_DURATION = 60


def notify_creator(poll):
    token = poll.hubot_token
    user_id = poll.user_id
    vchannel_id = get_p2p_vchannel_id(token, user_id)
    data = {
        'text': _('Poll Result'),
        "vchannel_id": vchannel_id,
        "form_url": url_for("poll.get_poll_result", poll_id=poll.id,
                            _external=True),
    }
    print('Send to {}'.format(user_id))
    send_message_to_bearychat(token, data)


def main():
    app = create_app()
    with app.test_request_context():
        expired_polls = Poll.get_multi_expired(EXPIRED_DURATION)
        print('Schedule: {}'.format(expired_polls))
        for poll in expired_polls:
            notify_creator(poll)


if __name__ == '__main__':
    main()
