import json
from flask import Flask, request
from db import db, Event, Club, User

from os import environ

app = Flask(__name__)
db_filename = 'events.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
 

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def root():
    return 'Cornell Club Events'
    
@app.route('/api/clubs/')
def get_all_clubs():
    clubs = Club.query.all()
    res = {'success': True, 'data': {"clubs": [club.serialize() for club in clubs]}}
    return json.dumps(res), 200

# @app.route('/api/clubs/goal/')
# def get_all_clubs():
#     clubs = Club.query.all()
#     res = {'clubs': [club.serialize() for club in clubs]}
#     return json.dumps(res), 200


@app.route('/api/user/<int:user_id>/clubs/', methods=['POST'])
def create_club(user_id):
    contents = json.loads(request.data)
    user = User.query.filter_by(id=user_id).first()
    club = Club(
        name = contents.get('name'),
        description = contents.get('description')
    )
    club.officers.append(user)
    club.users.append(user)
    db.session.add(club)
    db.session.commit()
    return json.dumps({'success': True, 'data': club.officers_serialize()}), 201

@app.route('/api/club/<int:club_id>/')
def get_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is None:
        return json.dumps({'success': False, 'error': "Club not found!"}), 404
    result = {'success': True, 'data': {"club" : club.members_serialize()}}
    return json.dumps(result), 200

@app.route('/api/user/<int:user_id>/clubs/')
def get_clubs_by_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return json.dumps({'success': False, 'data': 'User not found'}), 200
    clubs = user.clubs
    result = {'success': True, 'data': clubs}
    return json.dumps(result), 200

@app.route('/api/club/<int:club_id>/', methods=['DELETE'])
def delete_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        db.session.delete(club)
        db.session.commit()
        return json.dumps({'success': True, 'data': club.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Club not found!'}), 404

@app.route('/api/user/<int:user_id>/club/<int:club_id>/event/', methods=['POST'])
def create_event(user_id, club_id):
    club = Club.query.filter_by(id=club_id).first()
    user = User.query.filter_by(id=user_id).first()
    if club is None:
        return json.dumps({'success': False, 'error': 'Club not found'}), 404
    if user is None:
        return json.dumps({'success': False, 'error': 'User not found'}), 404
    content = json.loads(request.data)
    event = Event(
        club_id=club_id,
        description=content.get('description'),
        start_datetime=content.get('start_datetime'),
        end_datetime=content.get('end_datetime'),
    )
    for users in club.officers:
        if users.id == user.id:
            # event = Event(
            #     club_id=club_id,
            #     description=content.get('description'),
            #     start_datetime=content.get('start_datetime'),
            #     end_datetime=content.get('end_datetime'),
            # )
            db.session.add(event)
            db.session.commit()
            return json.dumps({'success': True, 'data': event.extended_serialize()}), 201
    return json.dumps({'success': False, 'error': 'User not authorized.'}), 404
    # db.session.add(event)
    # db.session.commit()
    # return json.dumps({'success': True, 'data': event.extended_serialize()}), 201

@app.route('/api/club/<int:club_id>/event/<int:event_id//')
def get_event_from_club(club_id, event_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is None:
        return json.dumps({'success': False, 'error': 'Club not found'}), 404
    if event_id >= len(club.events):
        return json.dumps({'success': False, 'error': "Event not found!"}), 404
    event = club.events[event_id]
    result = {'success': True, 'data': event.extended_serialize()}
    return json.dumps(result), 200

@app.route('/api/user/<int:user_id>/clubs/')
def get_all_events_by_club(club_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return json.dumps({'success': False, 'data': 'User not found'}), 200
    clubs = user.clubs
    result = {'success': True, 'data': clubs}
    return json.dumps(result), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    contents = json.loads(request.data)
    user = User(
        name=contents.get('name'),
        netid=contents.get('netid'),
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.extended_serialize()}), 201

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is not None:
        return json.dumps({'success': True, 'data': user.extended_serialize()}), 200
    return json.dumps({'success': False, 'data': 'User not found'}), 200

@app.route('/api/club/<int:club_id>/add/', methods=['POST'])
def add_user_to_club(club_id):
    contents = json.loads(request.data)
    user_type = contents.get('type', '')
    user_id = contents.get('user_id', '')

    user = User.query.filter_by(id=user_id).first()
    club = Club.query.filter_by(id=club_id).first()

    if user is None or club is None:
        return json.dumps({'success': False, 'error': 'Club or User not found'}), 404
    
    if user_type == 'member':
        club.members.append(user)
    else:
        club.officers.append(user)

    db.session.add(club)
    db.session.commit()
    
    if user_type == 'member':
        return json.dumps({'success': True, 'data': club.members_serialize()}), 200
    else:
        return json.dumps({'success': True, 'data': club.officers_serialize()}), 200

# @app.route('/api/user/<int:user_id>/club/<int:club_id>/event/<int:event_id>/', methods=['DELETE'])
# def delete_event(user_id, club_id, event_id):
#     club = Club.query.filter_by(id=club_id).first()
#     user = User.query.filter_by(id=user_id).first()
#     if club is None:
#         return json.dumps({'success': False, 'error': 'Club not found'}), 404
#     if user is None:
#         return json.dumps({'success': False, 'error': 'User not found'}), 404
#     if user.name 
#     # if event_id >= len(club.events):
#     #     return json.dumps({'success': False, 'error': "Event not found!"}), 404
#     # event = club.events[event_id]
#     # result = {'success': True, 'data': event.extended_serialize()}
#     # return json.dumps(result), 200
#     if event_id < len(club.events):
#         db.session.delete(event)
#         db.session.commit()
#         return json.dumps({'success': True, 'data': event.serialize()}), 200
#     return json.dumps({'success': False, 'error': 'Event not found!'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
