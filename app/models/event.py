from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime
from typing import Optional
from models.user import User


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