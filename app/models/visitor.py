from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey


class Visitor(db.Model):
    __tablename__ = 'visitor'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    user_email:Mapped[str]
    phone:Mapped[int]
    event_id:Mapped[int] = mapped_column(ForeignKey('event.id'))



