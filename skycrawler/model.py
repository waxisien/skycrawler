from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
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
	creation_date = Column(DateTime)

	city = relationship('City')

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

	def __repr__(self):
		return '<City %r>' % self.name

	def __str__(self):
		return self.name
