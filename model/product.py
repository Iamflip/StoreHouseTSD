from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base

class Product(Base):
    __tablename__ = "reconciliaition_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reconciliation_id = Column(Integer, ForeignKey("reconciliation.id"), nullable=False)
    product_name = Column(String, nullable=False)
    product_rid = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    reconciliation = relationship("Reconciliation", back_populates="products")