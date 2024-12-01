from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean
from datetime import datetime   
from typing import  Optional, List

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class Role(db.Model):
    __tablename__='role_table'

    role_id:Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    name:Mapped[str]= mapped_column(String, unique=True)
    description:Mapped[str] = mapped_column(String(length=288))
    users: Mapped[List['User']] = relationship('User', back_populates='role')


class User(db.Model, UserMixin):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    username: Mapped[Optional[str]] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_pic: Mapped[Optional[str]] = mapped_column(String) 
    bio: Mapped[Optional[str]] = mapped_column(String)  
    events: Mapped[List['Event']] = relationship('Event', back_populates='user', lazy="dynamic")  
    user_role_id: Mapped[int] = mapped_column(ForeignKey('role_table.role_id'))  
    role:Mapped['Role'] = relationship('Role', back_populates='users')
    fs_uniquifier: Mapped[str] = mapped_column(String, unique=True, nullable=False)
     


    @validates('email')
    def validate_email(self, key, email:str)->str:
        if db.session.query(User).filter_by(email=email).first():
            raise ValueError("Email already Exist")
        return email
    

    @validates('username')
    def validate_username(self, key, username:str) ->str:
        if db.session.query(User).filter_by(username=username).first():
            raise ValueError("User already Exist")
        return username
    

    
    
        

class Event(db.Model):
    __tablename__ = 'event'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String) 
    location: Mapped[Optional[str]] = mapped_column(String)  
    category: Mapped[Optional[str]] = mapped_column(String)  
    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id'))
    user: Mapped['User'] = relationship('User', back_populates='events')  

    @validates('date')
    def validate_date(self, key, date):
        if date > datetime.now():
            raise ValueError("Event date must be in the future.")
        return date


class Visitor(db.Model):
    __tablename__ = 'visitor'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_email:Mapped[str]
    phone:Mapped[str] = mapped_column(String, nullable=False)
    event_id:Mapped[int] = mapped_column(ForeignKey('event.id'))

    @validates('user_email')
    def validate_user_email(self, key, email:str) -> str:
        if db.session.query(User).filter_by(email=email).first() is None:
            raise ValueError("Email must be associated with a registered user.")
        return email

    @validates('phone')
    def validate_phone(self, key, phone):
        if not phone.isdigit() or len(phone) < 10:
            raise ValueError("Phone number must be at least 10 digits long and numeric.")
        return phone
    



