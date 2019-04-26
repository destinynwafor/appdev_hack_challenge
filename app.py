import json
from flask import Flask, request
from db import db, Event, Club, User

app = Flask(__name__)
db_filename = 'events.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
 

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')

@app.route('/api/clubs/')
def get_all_clubs():
    clubs = Club.query.all()
    club_list = []
    for club in clubs:
        club_list.append(club.serialize())
    res = {'success': True, 'data': club_list}
    return json.dumps(res), 200

@app.route('/api/clubs/', methods=['POST'])
def create_club():
    contents = json.loads(request.data)
    club = Club(
        name = contents.get('name'),
        description = contents.get('description')
    )
    db.session.add(club)
    db.session.commit()
    return json.dumps({'success': True, 'data': club.serialize()}), 201

@app.route('/api/club/<int:club_id>/')
def get_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is None:
        return json.dumps({'success': False, 'error': "Club not found!"}), 404
    result = {'success': True, 'data': club.serialize()}
    return json.dumps(result), 200

@app.route('/api/club/<int:club_id>/', methods=['DELETE'])
def delete_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if club is not None:
        db.session.delete(club)
        db.session.commit()
        return json.dumps({'success': True, 'data': club.serialize()}), 200
    return json.dumps({'success': False, 'error': 'Club not found!'}), 404
    
@app.route('/')
def root():
    return 'Hello world!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
