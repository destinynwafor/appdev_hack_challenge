import json
from flask import Flask, request
from db import db, Assignment, Class, User

app = Flask(__name__)
db_filename = 'cms.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return 'Hello world!'

@app.route('/api/classes/')
def get_classes():
    classes = Class.query.all()
    res = {
        'success': True,
        'data': [c.serialize() for c in classes]
    }
    return json.dumps(res), 200

@app.route('/api/classes/', methods=['POST'])
def create_class():
    post_body = json.loads(request.data)
    new_class = Class(
        code=post_body.get('code'),
        name=post_body.get('name')
    )
    db.session.add(new_class)
    db.session.commit()
    return json.dumps({'success': True, 'data': new_class.serialize()}), 201

@app.route('/api/class/<int:class_id>/')
def get_class(class_id):
    optional_class = Class.query.filter_by(id=class_id).first()
    if optional_class is not None:
        return json.dumps({'success': True, 'data': optional_class.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Class not found'}), 404

@app.route('/api/class/<int:class_id>/', methods=['DELETE'])
def delete_class(class_id):
    optional_class = Class.query.filter_by(id=class_id).first()
    if optional_class is not None:
        db.session.delete(optional_class)
        db.session.commit()
        return json.dumps({'success': True, 'data': optional_class.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Class not found'}), 404

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    new_user = User(
        name=post_body.get('name'),
        netid=post_body.get('netid'),
    )
    db.session.add(new_user)
    db.session.commit()
    return json.dumps({'success': True, 'data': new_user.serialize()}), 201

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    optional_user = Class.query.filter_by(id=user_id).first()
    if optional_user is not None:
        return json.dumps({'success': True, 'data': optional_user.serialize()}), 200
    return json.dumps({'success': False, 'data': 'User not found'}), 200
    
@app.route('/api/class/<int:class_id>/add/', methods=['POST'])
def add_user_to_class(class_id):
    post_body = json.loads(request.data)
    user_type = post_body.get('type', '')
    user_id = post_body.get('user_id', '')

    optional_user = User.query.filter_by(id=user_id).first()
    optional_class = Class.query.filter_by(id=class_id).first()

    if optional_user is None or optional_class is None:
        return json.dumps({'success': False, 'error': 'Class or User not found'}), 404
    
    if user_type == 'student':
        optional_class.students.append(optional_user)
    else:
        optional_class.instructors.append(optional_user)

    db.session.add(optional_class)
    db.session.commit()
    return json.dumps({'success': True, 'data': optional_class.serialize()}), 200

@app.route('/api/class/<int:class_id>/assignment/', methods=['POST'])
def create_assignment(class_id):
    optional_class = Class.query.filter_by(id=class_id).first()
    if optional_class is None:
        return json.dumps({'success': False, 'error': 'Class not found'}), 404

    post_body = json.loads(request.data)
    new_assignment = Assignment(
        class_id=class_id,
        description=post_body.get('description'),
        due_date=post_body.get('due_date'),
    )
    db.session.add(new_assignment)
    db.session.commit()
    return json.dumps({'success': True, 'data': new_assignment.serialize()}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
