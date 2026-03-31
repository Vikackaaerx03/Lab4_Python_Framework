from datetime import date
import re

from pydantic import BaseModel, validator


class OrderBase(BaseModel):
    order_number: str
    customer_name: str
    total_price: float
    order_date: date

    @validator("order_number")
    def validate_order_number(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Order number cannot be empty")
        if len(value) != 3:
            raise ValueError("Order number must contain exactly 3 digits")
        if not re.fullmatch(r"\d{3}", value):
            raise ValueError("Order number must be in format 001")
        if value == "000":
            raise ValueError("Order number must start from 001")
        return value

    @validator("customer_name")
    def validate_customer_name(cls, value: str) -> str:
        value = " ".join(value.split())
        if not value:
            raise ValueError("Customer name cannot be empty")
        if len(value) < 2:
            raise ValueError("Customer name is too short")
        if len(value) > 100:
            raise ValueError("Customer name is too long")
        return value

    @validator("total_price")
    def validate_total_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Total price must be greater than 0")
        return value

    @validator("order_date")
    def validate_order_date(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Order date cannot be in the future")
        return value


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    id: int

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    message: str


class NextOrderNumberResponse(BaseModel):
    next_order_number: str
