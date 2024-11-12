from app import app, db
from app.models.event import Event
from flask import  render_template, request, jsonify, make_response, session
from  datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def home_page():
    date = request.args.get('date')
    
    return render_template('pages/home.html')



@app.route('/event', methods=['GET', 'POST'])
def event_page():
    data = Event.query.all()
    if request.method == 'POST':
        visitor = request.form.to_dict()
        
        return jsonify({"message":"You've registered succesfully!"}), 201            
    return render_template('pages/event.html', event=data)

        


@app.route('/event/<int:id>', methods=['PUT'])
def update_event(id):
    event = request.get_json()
    existing_event = Event.query.get(id)
    if not existing_event:
        return jsonify({'message':'Event not found!'}), 404
    
    if not event or 'name' not in event or 'date' not in event:
        return jsonify({'message': 'Invalid input!'}), 400
    try:
        event_date = datetime.strptime( event['date'], '%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        return jsonify({'message': f'Invalid date format! {e}'}), 400
    existing_event.name = event['name']
    existing_event.date = event_date,
    existing_event.description = event['description'],
    existing_event.location = event['location'],
    existing_event.category = event['catergory']
    db.session.commit()
    return jsonify({'message': 'Event updated successfully!'}), 200


@app.route('/event/<int:id>', methods=['DELETE'])
def remove_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'message': 'Event not found!'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully!'}), 200

    
@app.route('/createevent', methods=['POST', 'GET'])
def add_event():
    if request.method == 'POST':
        event = request.form.to_dict()
       
        if not event or 'name' not in event or 'date' not in event:
            return jsonify({'message': 'Invalid input!'}), 400
        try:
            event_date = datetime.strptime( event['date'], '%Y-%m-%dT%H:%M')
        except ValueError as e:
            return jsonify({'message': f'Invalid date format! {e}'}), 400
        data = Event(
            name=event['name'],
            date= event_date,
            description = event['description'],
            location = event['location'],
            category = event['category']
        )
        db.session.add(data)
        db.session.commit()
        return jsonify({'message':'Event added successfully!'}), 201
    return render_template('pages/create-event.html')


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('errors/not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.errorhandler(404)
def invalid_input(error):
    resp = make_response(render_template('errors/invalid-input.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp