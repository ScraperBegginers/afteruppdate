from . import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    spins = db.Column(db.Integer, default=0)
    daily_spin = db.Column(db.Float, default=0)
    my_referral = db.Column(db.Integer, default=0)
    get_bonus_for_two_friends = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'spins': self.spins,
            'daily_spin': self.daily_spin,
            'my_referral': self.my_referral,
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


