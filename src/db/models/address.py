from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db.base_class import Base


class Address(Base):
    """ table field names for address"""
    __tablename__ = "address"
    coordinates = Column(String)
    address_body = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="address")


class User(Base):
    """table field names for user"""
    __tablename__ = 'users'
    name = Column(String)
    email = Column(String)
    password = Column(String)
    address = relationship("Address", back_populates="creator")
