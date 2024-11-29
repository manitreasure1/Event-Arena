from app import app, db
from app.database import Event, User, Visitor, Role
from flask import  render_template, request, jsonify, redirect, url_for, flash
from  datetime import datetime
from app.forms import SignUp, Login, Admin
import asyncio
from app import bcrypt
from app.utils import username
import secrets
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, set_access_cookies ,unset_jwt_cookies


@app.route('/', methods=['GET', 'POST'])
async def home_page():
    date = request.args.get('date')
    event_date = Event.query.filter_by(date=date).all
    return render_template('pages/home.html')


@app.route('/event', methods=['GET', 'POST'])
@jwt_required()
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
    role = Role.query.get({'role_id': 2})
    if form.validate_on_submit():
        user = User(
            username=username(form.email.data),
            email=form.email.data,
            password= bcrypt.generate_password_hash(form.password.data),
            role=role,
            fs_uniquifier = secrets.token_urlsafe(32)
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
        user = User.query.filter_by(email= form.email.data).first()
        password =  bcrypt.check_password_hash(user.password, form.password.data)
        access_token = create_access_token(identity=user.username)
        if not user:
            flash("Invalid credentials", category="danger")
        elif not password:
            flash("Invalid credentials", category="danger")
        else:
            flash("You've Logged in successfully", "success")
            res = redirect(url_for('event_page'))
            set_access_cookies(response=res, encoded_access_token=access_token)
            # print(res.headers)
            return res
    return render_template('includes/login.html', form=form)


@app.route('/createevent', methods=['POST', 'GET'])
@jwt_required(refresh=True)
def add_event():
    current_user_id = get_jwt_identity()
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
            date=event_date,
            description=event['description'],
            location=event['location'],
            category=event['category'],
            user=current_user_id
        )
        db.session.add(data)
        db.session.commit()
        return jsonify({'message':'Event added successfully!'}), 201
    return render_template('pages/create-event.html')

# Todo
@jwt_required()
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


# todo
@jwt_required
@app.route('/event/<int:id>', methods=['DELETE'])
def remove_event(id):
    event = Event.query.get(id)
    if not event:
        return jsonify({'message': 'Event not found!'}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({'message': 'Event deleted successfully!'}), 200


#todo
@app.route("/logout")
def logout_page():
    unset_jwt_cookies()
    return redirect(url_for('login'))


@app.route("/adminlog")
def admin_page_login():
    form = Admin()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and  user.password == form.password.data:
            return redirect(url_for('admin.html'))
        else:
            flash('You are not qualified or incorrect credentials.')
    return render_template('pages/adminlog.html', form=form)


# Todo 
@app.route("/logout")
def admin_logout_page():
    unset_jwt_cookies()
    return redirect(url_for('admin_page_login'))
