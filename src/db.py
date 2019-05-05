from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

student_association_table = db.Table(
    'students',
    db.Model.metadata,
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

instructor_association_table = db.Table(
    'instructors',
    db.Model.metadata,
    db.Column('instructor_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
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

class Class(db.Model):
    __tablename__ = 'class'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    assignments = db.relationship('Assignment', cascade='delete')

    students = db.relationship("User", secondary=student_association_table)
    instructors = db.relationship("User", secondary=instructor_association_table)

    def  __init__(self, **kwargs):
        self.code = kwargs.get('code', '')
        self.name = kwargs.get('name', '')

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'assignments': [a.serialize() for a in self.assignments],
            'students': [s.serialize() for s in self.students],
            'instructors': [i.serialize() for i in self.instructors],
        }

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    def __init__(self, **kwargs):
        self.description = kwargs.get('description', '')
        self.due_date = kwargs.get('due_date', 0)
        self.class_id = kwargs.get('class_id')

    def serialize(self):
        return {
            'id': self.id,
            'description': self.description,
            'due_date': self.due_date,
        }
