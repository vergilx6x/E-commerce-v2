from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from api.app.models.base_model import BaseModel, Base


class Favorite(BaseModel, Base):
    """ Represents a favorite product for a user """
    __tablename__ = 'favorites'

    # Assuming BaseModel has id, created_at, and updated_at
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    product_id = Column(String(60), ForeignKey('products.id'), nullable=False)

    user = relationship("User", back_populates="favorites")
    product = relationship("Product", back_populates="favorites")
