from . import db
from sqlalchemy import Column, Integer, String, Boolean, Float, text
from time import time

class User(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    firstname = Column(String(50), nullable=False, server_default=text("'Unknown'"))
    username = Column(String(80), nullable=False, server_default=text("'anonymous'"))
    spins = Column(Integer, default=0, nullable=False, server_default=text("0"))
    daily_spin = Column(Float, default=0.0, nullable=False, server_default=text("0.0"))
    my_referral = Column(Integer, default=0, nullable=False, server_default=text("0"))
    get_bonus_for_two_friends = Column(Boolean, default=False, nullable=False, server_default=text("0"))
    total_spins = Column(Integer, default=0, nullable=False, server_default=text("0"))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'firstname': self.firstname,
            'username': self.username,
            'spins': self.spins,
            'daily_spin': self.daily_spin,
            'my_referral': self.my_referral,
            'total_spins': self.total_spins,
            'get_bonus_for_two_friends': self.get_bonus_for_two_friends
        }


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'link': self.link,
        }

class TasksCompleted(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'link': self.link,
            'user_id': self.user_id,
        }

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_manager = db.Column(db.String(255), nullable=False, default="https://google.com")
    link_partner = db.Column(db.String(255), nullable=False, default="https://google.com")
    link_gift = db.Column(db.String(255), nullable=False, default="https://google.com")

    def to_dict(self):
        return {
            'link_manager': self.link_manager,
            'link_partner': self.link_partner,
            'link_gift': self.link_gift,
        }


class SubscribeChecker(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    channel_id = Column(Integer, nullable=False)
    time_wait = Column(Float, default=time(), server_default=text(str(time())))
    status_sub = Column(Boolean, server_default=text('0'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'channel_id': self.channel_id,
            'time_wait': self.time_wait,
            'status_sub': self.status_sub,
        }