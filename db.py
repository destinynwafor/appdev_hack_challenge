from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


member_association_table = db.Table('members', db.Model.metadata,
    db.Column('member_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

officer_association_table = db.Table('officers', db.Model.metadata,
    db.Column('officer_id', db.Integer, db.ForeignKey('user.id')),
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
    type_ = db.Column(db.String, nullable=False)
    
    clubs = db.relationship('Club', secondary=member_association_table) #, back_populates='users')

    def  __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        self.type_ = kwargs.get('type', '')

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
            'clubs': [event.serialize() for event in self.events if event.id > 0],
            'members': [member.serialize() for member in self.users if member.type_ == "member"]
        }

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    
    events = db.relationship('Event', cascade='delete') #one-to-many so events should not exist without a club
    users = db.relationship('User', secondary=officer_association_table) #, back_populates='clubs' #many-to-many relationship so association table needed

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
            'officers': [officer.serialize() for officer in self.users if officer.type_ == "officer"],
            'events': [event.serialize() for event in self.events if event.id > 0]
        }

    def officers_serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'officers': [officer.serialize() for officer in self.users if officer.type_ == "officer"],
            'members': [member.serialize() for member in self.users if member.type_ == "member"],
            'events': [event.serialize() for event in self.events if event.id > 0]
        }

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False) #UTC formatted string 
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)

    attendees = db.relationship('User', secondary=attendee_association_table) #, back_populates='clubs')

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', '')
        self.date = kwargs.get('date', "1") 
        self.start_time = kwargs.get('time', '10')
        self.end_time = kwargs.get('time', '10')
        self.club_id = kwargs.get('club_id')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time
        }
    
    def extended_serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'attendees': [attendee.serialize() for attendee in self.events if event.id > 0]
        }
    