from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()


student_association_table = db.Table('students', db.Model.metadata,
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

officer_association_table = db.Table('officers', db.Model.metadata,
    db.Column('officer_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

attendee_association_table = db.Table('attendees', db.Model.metadata,
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)

    def  __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
        }

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    events = db.relationship('Event', cascade='delete')

    students = db.relationship("User", secondary=student_association_table)
    officers = db.relationship("User", secondary=officer_association_table)

    def  __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.description = kwargs.get('description', '')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'officers': [of.serialize() for of in self.officers],
            'events': [ev.serialize() for ev in self.events],
            #'students': [st.serialize() for st in self.students],
        }

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False) #UTC formatted string 
    start_time = db.Column(db.Integer, nullable=False)
    end_time = db.Column(db.Integer, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)

    attendees = db.relationship("User", secondary=attendee_association_table)

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', '')
        self.date = kwargs.get('date', "1") 
        self.start_time = kwargs.get('time', 10)
        self.end_time = kwargs.get('time', 10)
        self.club_id = kwargs.get('club_id')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'attendees': [at.serialize() for at in self.attendees],
        }
