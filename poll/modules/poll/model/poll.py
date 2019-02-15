# -*- coding: utf-8 -*-

from __future__ import absolute_import

from datetime import datetime
import json

from poll.extensions import db


class Poll(db.Model):

    __tablename__ = 'poll'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    option_count = db.Column(db.Integer)
    is_anonymous = db.Column(db.Boolean)
    end_datetime = db.Column(db.DateTime)
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
