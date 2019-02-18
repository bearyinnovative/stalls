# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datetime import datetime
import json

from poll.extensions import db


class Poll(db.Model):

    __tablename__ = 'poll'

    STATE_CREATED = 'created'
    STATE_SENT = 'sent'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    option_count = db.Column(db.Integer)
    is_anonymous = db.Column(db.Boolean)
    end_datetime = db.Column(db.DateTime)
    message_key = db.Column(db.String(64))
    state = db.Column(db.String(32), default=STATE_CREATED)
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
    def get_multi_by_poll_id(cls, poll_id):
        return cls.query.filter_by(poll_id=poll_id).all()


class UserSelection(db.Model):

    __tablename__ = 'user_selection'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer,)
    user_id = db.Column(db.Integer,)
    poll_id = db.Column(db.Integer,)
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
