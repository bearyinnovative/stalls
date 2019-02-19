# -*- coding: utf-8 -*-

from __future__ import absolute_import

import binascii
from datetime import datetime
import json
import os

from stalls.extensions import db


def gen_visit_key():
    return binascii.hexlify(os.urandom(32)).decode()


class Poll(db.Model):

    __tablename__ = 'poll'

    STATE_CREATED = 'created'
    STATE_SENT = 'sent'

    id = db.Column(db.Integer, primary_key=True)
    hubot_token = db.Column(db.String(64))
    user_id = db.Column(db.String(32),)
    team_id = db.Column(db.String(32),)
    description = db.Column(db.String(64))
    option_count = db.Column(db.Integer)
    is_anonymous = db.Column(db.Boolean)
    end_datetime = db.Column(db.DateTime)
    message_key = db.Column(db.String(64))
    state = db.Column(db.String(32), default=STATE_CREATED)
    visit_key = db.Column(db.String(64), default=gen_visit_key)
    _options = db.Column('options', db.String(10240))
    _members = db.Column('members', db.String(10240))
    _channels = db.Column('channels', db.String(10240))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def options(self):
        return json.loads(self._options)

    @options.setter
    def options(self, value):
        self._options = json.dumps(value)

    @property
    def members(self):
        return json.loads(self._members)

    @members.setter
    def members(self, value):
        self._members = json.dumps(value)

    @property
    def channels(self):
        return json.loads(self._channels)

    @channels.setter
    def channels(self, value):
        self._channels = json.dumps(value)

    def save(self, _commit=True):
        try:
            db.session.add(self)
            if _commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_multi_by_ids(cls, ids):
        return cls.query.filter(Poll.id.in_(ids)).all()

    @classmethod
    def get_multi_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def count_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).count()

    @classmethod
    def get_by_id_and_visit_key(cls, poll_id, vk):
        return cls.query.filter_by(id=poll_id, visit_key=vk).first()


class PollOption(db.Model):

    __tablename__ = 'poll_option'

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(64))
    poll_id = db.Column(db.Integer)

    def save(self, _commit=True):
        try:
            db.session.add(self)
            if _commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_multi_by_poll_id(cls, poll_id, _execute=True):
        q = cls.query.filter_by(poll_id=poll_id)
        if _execute:
            return q.all()
        return q


class UserSelection(db.Model):

    __tablename__ = 'user_selection'

    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer,)
    team_id = db.Column(db.String(32),)
    user_id = db.Column(db.String(32),)
    option_id = db.Column(db.Integer,)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self, _commit=True):
        try:
            db.session.add(self)
            if _commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_multi_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def count_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).count()

    @classmethod
    def count_by_poll_id_and_option_id(cls, poll_id, option_id):
        return cls.query.filter_by(poll_id=poll_id,
                                   option_id=option_id).count()

    @classmethod
    def get_by_poll_id_and_user_id(cls, poll_id, user_id):
        return cls.query.filter_by(
            poll_id=poll_id,
            user_id=user_id
        ).first()
