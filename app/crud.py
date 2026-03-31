from sqlalchemy.orm import Session

from app.models import Order


def get_orders(db: Session):
    return db.query(Order).order_by(Order.id).all()


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_by_number(db: Session, order_number: str):
    return db.query(Order).filter(Order.order_number == order_number).first()


def get_next_order_number(db: Session) -> str:
    orders = db.query(Order.order_number).all()
    numeric_values = set()

    for (order_number,) in orders:
        if order_number and order_number.isdigit() and len(order_number) == 3:
            numeric_values.add(int(order_number))

    next_number = 1
    while next_number in numeric_values:
        next_number += 1

    return f"{next_number:03d}"


def create_order(db: Session, data):
    order = Order(**data.dict())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_order(db: Session, order_id: int, data):
    order = get_order(db, order_id)
    if order:
        order.order_number = data.order_number
        order.customer_name = data.customer_name
        order.total_price = data.total_price
        order.order_date = data.order_date
        db.commit()
        db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = get_order(db, order_id)
    if order:
        db.delete(order)
        db.commit()
    return order
