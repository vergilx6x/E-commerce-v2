#!/usr/bin/python3
""" holds class Order"""

from api.app.models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):

    __tablename__ = 'orders'
    user_id = Column(String(128), ForeignKey('users.id'), nullable=True)
    status = Column(String(64), nullable=False, default="pending")
    total_amount = Column(Integer, nullable=True)
    user = relationship("User", backref="orders")

    order_items = relationship("Order_item", back_populates="order",
                               cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes product"""
        super().__init__(*args, **kwargs)
