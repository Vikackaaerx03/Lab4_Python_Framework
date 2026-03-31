from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import (
    MessageResponse,
    NextOrderNumberResponse,
    OrderCreate,
    OrderResponse,
)

router = APIRouter(prefix="/api/orders", tags=["orders-api"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[OrderResponse])
def read_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@router.get("/meta/next-number", response_model=NextOrderNumberResponse)
def get_next_order_number(db: Session = Depends(get_db)):
    return NextOrderNumberResponse(next_order_number=crud.get_next_order_number(db))


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    existing_order = crud.get_order_by_number(db, data.order_number)
    if existing_order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order number already exists",
        )

    expected_order_number = crud.get_next_order_number(db)
    if data.order_number != expected_order_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Next order number must be {expected_order_number}",
        )

    return crud.create_order(db, data)


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, data: OrderCreate, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    existing_order = crud.get_order_by_number(db, data.order_number)
    if existing_order and existing_order.id != order_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order number already exists",
        )

    updated_order = crud.update_order(db, order_id, data)
    return updated_order


@router.delete("/{order_id}", response_model=MessageResponse)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return MessageResponse(message=f"Order {order_id} deleted successfully")


@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order
