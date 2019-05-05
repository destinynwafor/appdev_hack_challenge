from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


member_association_table = db.Table('members', db.Model.metadata,
    db.Column('member_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

officer_association_table = db.Table('officers', db.Model.metadata,
    db.Column('officer_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

user_association_table = db.Table('users', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

attendee_association_table = db.Table('attendees', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    # type_ = db.Column(db.String, nullable=False)
    
    clubs = db.relationship('Club', secondary=member_association_table) #, back_populates='users')
    events = db.relationship("Event", secondary=attendee_association_table)

    def  __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        # self.type_ = kwargs.get('type', '')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
        }

    def extended_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
            'clubs': [cl.serialize() for cl in self.clubs],
            'events': [ev.serialize() for ev in self.events],        
        }

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    events = db.relationship('Event', cascade='delete') #one-to-many so events should not exist without a club
    members = db.relationship("User", secondary=member_association_table)
    officers = db.relationship("User", secondary=officer_association_table)
    users = db.relationship("User", secondary=user_association_table)

    def  __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    def members_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'officers': [of.serialize() for of in self.officers],
            'events': [ev.serialize() for ev in self.events],
        }

    def officers_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'officers': [of.serialize() for of in self.officers],
            'members': [me.serialize() for me in self.members],
            'events': [ev.serialize() for ev in self.events],
        }

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    start_datetime = db.Column(db.String, nullable=False) #UTC formatted string 
    end_datetime = db.Column(db.String, nullable=False) #UTC formatted string 
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)

    attendees = db.relationship('User', secondary=attendee_association_table) #, back_populates='clubs')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', '')
        self.start_datetime = kwargs.get('start_datetime', '10')
        self.end_datetime = kwargs.get('end_datetime', '10')
        self.club_id = kwargs.get('club_id')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            # 'start_datetime': self.start_datetime,
            # 'end_datetime': self.end_datetime,
        }
    
    def extended_serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'start_datetime': self.start_datetime,
            'end_datetime': self.end_datetime,
            'attendees': [at.serialize() for at in self.attendees],
        }
    