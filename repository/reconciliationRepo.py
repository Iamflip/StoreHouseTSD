from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import text

from dto.productDto import ProductDto
from model.reconciliation import Reconciliation
from model.product import Product

import logging
logging.basicConfig(level=logging.INFO)

def create_reconciliation(db: Session, date_created: str, place_rid: int, place_name: str, products: list):
    try:
        reconciliation = Reconciliation(date_created=date_created, place_rid=place_rid, place_name=place_name)
        db.add(reconciliation)
        db.flush()  # Записываем без коммита

        reconciliation_products = [
            Product(
                reconciliation_id=reconciliation.id,
                product_name=product.product_name,
                product_rid=product.product_rid,
                quantity=product.quantity
            )
            for product in products
        ]
        db.add_all(reconciliation_products)

        db.commit()
        db.refresh(reconciliation)

        return reconciliation

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        db.rollback()
        raise e


def get_reconciliation_by_id(db: Session, reconciliation_id: int):
    return db.query(Reconciliation).filter(Reconciliation.id == reconciliation_id).first()

def get_all_reconciliation(db: Session):
    return db.query(Reconciliation).filter(Reconciliation.uploaded == False).all()

def update_reconciliation(db: Session, reconciliation_id: int, new_products: list[ProductDto]):
    try:
        db.execute(text("BEGIN EXCLUSIVE TRANSACTION;"))

        existing_products = db.query(Product).filter(Product.reconciliation_id == reconciliation_id).all()
        product_map = {p.product_rid: p for p in existing_products}

        for new_product in new_products:
            if new_product.product_rid in product_map:
                product_map[new_product.product_rid].quantity += new_product.quantity
            else:
                db.add(Product(
                    reconciliation_id=reconciliation_id,
                    product_name=new_product.product_name,
                    product_rid=new_product.product_rid,
                    quantity=new_product.quantity
                ))

        db.commit()
        return db.query(Reconciliation).filter(Reconciliation.id == reconciliation_id).first()

    except IntegrityError:
        db.rollback()
        return {"status": "error", "message": "Ошибка добавления товаров (возможно, конфликт записей)"}

def upload_reconciliation(db: Session, reconciliation_id: int):
    reconciliation = db.query(Reconciliation).filter(Reconciliation.id == reconciliation_id).first()
    reconciliation.uploaded = True

    db.commit()
    db.refresh(reconciliation)
    return reconciliation
