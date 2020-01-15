from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Brief(Base):
    __tablename__ = 'brief'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    is_active = Column(Boolean)
    name = Column(String)
    question = relationship('Question')

class Question(Base):

    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    brief_id = Column(Integer, ForeignKey('brief.id'))
    text = Column(String)
