from app import app, db
from app.database import Event, User, Visitor
from flask import  render_template, request, jsonify, make_response, session, redirect, url_for, flash
from  datetime import datetime
from app.forms import SignUp, Login
import asyncio



@app.route('/', methods=['GET', 'POST'])
async def home_page():
    date = request.args.get('date')
    event_date = Event.query.filter_by(date=date).all
    
    return render_template('pages/home.html')



@app.route('/event', methods=['GET', 'POST'])
async def event_page():
    data = Event.query.all()
    await asyncio.sleep(1)
    if request.method == 'POST':
        visitor = request.form.to_dict()
        registerer = Visitor(
            email=visitor.email,
            phone=visitor.phone
        )
        db.session.add(registerer)
        db.session.commit()
        
        return jsonify({"message":"You've registered succesfully!"}), 201            
    return render_template('pages/event.html', event=data)


@app.route('/signup', methods=['POST', 'GET'])
def signUp():
    form = SignUp()
    if form.validate_on_submit():
        user = User(
            username=(form.first_name.data[:3]+form.last_name.data[:3]),
            email=form.email.data,
            password=form.password.data,          
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created Successfully", category="success")
        return redirect(url_for("event_page"))
    else:
        print(form.errors)
    return render_template('includes/signUp.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if form.validate_on_submit():
        email = User.query.filter_by("email")
        password = form.password.data
        try:
            if any(email == form.email.data):
                return jsonify({"message":"You've Logged in successfully"})
        except Exception as e:     
            return jsonify({"message": f"{e}"})
        return redirect(url_for('event_page'))
    return render_template('includes/login.html', form=form)



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
    return resp


@app.errorhandler(404)
def invalid_input(error):
    resp = make_response(render_template('errors/invalid-input.html'), 404)
    
    return resp