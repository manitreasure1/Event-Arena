from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import Optional, List
from models.event import Event
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