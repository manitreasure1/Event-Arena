from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey
from datetime import datetime   
from typing import Optional, List
from app.utils import Role

class User(db.Model):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    profile_pic: Mapped[Optional[str]] = mapped_column(String) 
    role: Mapped[str] = mapped_column(String, default=Role)  
    bio: Mapped[Optional[str]] = mapped_column(String)  
    events: Mapped[List['Event']] = relationship('Event', back_populates='user')  


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


class Visitor(db.Model):
    __tablename__ = 'visitor'

    id:Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_email:Mapped[str]
    phone:Mapped[str]
    event_id:Mapped[int] = mapped_column(ForeignKey('event.id'))
