from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db.database import Base

class Reconciliation(Base):
    __tablename__ = "reconciliation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_created = Column(String, nullable=False)
    place_rid = Column(Integer, nullable=False)
    place_name = Column(String, nullable=False)
    uploaded = Column(Boolean, default=False)

    products = relationship("Product", back_populates="reconciliation")