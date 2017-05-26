from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Building(Base):
    __tablename__ = "building"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    height = Column(Integer)
    floors = Column(Integer)
    link = Column(String())
    city_id = Column(Integer, ForeignKey('city.id'))
    status = Column(String())
    is_active = Column(Boolean, default=True)
    creation_date = Column(DateTime)

    city = relationship('City')

    def __init__(self, name, height, floors, link, city, status, is_active):
        self.name = name
        self.height = height
        self.floors = floors
        self.link = link
        self.city = city
        self.status = status
        self.is_active = is_active
        self.creation_date = datetime.now()

    def __repr__(self):
        return '<Building %r>' % self.name

    def __str__(self):
        return self.name


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    latitude = Column(Float)
    longitude = Column(Float)
    creation_date = Column(DateTime)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.creation_date = datetime.now()

    def __repr__(self):
        return '<City %r>' % self.name

    def __str__(self):
        return self.name
