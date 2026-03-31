from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud
from app.database import SessionLocal
from app.schemas import OrderCreate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
def read_orders(request: Request, db: Session = Depends(get_db)):
    orders = crud.get_orders(db)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "orders": orders,
        },
    )


@router.get("/create", response_class=HTMLResponse)
def create_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "create.html",
        {
            "request": request,
            "error": None,
            "form_data": {},
            "expected_order_number": crud.get_next_order_number(db),
        },
    )


@router.post("/create")
def create_order(
    request: Request,
    order_number: str = Form(...),
    customer_name: str = Form(...),
    total_price: str = Form(...),
    order_date: str = Form(...),
    db: Session = Depends(get_db),
):
    form_data = {
        "order_number": order_number,
        "customer_name": customer_name,
        "total_price": total_price,
        "order_date": order_date,
    }

    try:
        data = OrderCreate(**form_data)
    except ValidationError as exc:
        return templates.TemplateResponse(
            "create.html",
            {
                "request": request,
                "error": exc.errors()[0]["msg"],
                "form_data": form_data,
                "expected_order_number": crud.get_next_order_number(db),
            },
            status_code=422,
        )

    existing_order = crud.get_order_by_number(db, data.order_number)
    if existing_order:
        return templates.TemplateResponse(
            "create.html",
            {
                "request": request,
                "error": "Order number already exists",
                "form_data": form_data,
                "expected_order_number": crud.get_next_order_number(db),
            },
            status_code=422,
        )

    expected_order_number = crud.get_next_order_number(db)
    if data.order_number != expected_order_number:
        return templates.TemplateResponse(
            "create.html",
            {
                "request": request,
                "error": f"Next order number must be {expected_order_number}",
                "form_data": form_data,
                "expected_order_number": expected_order_number,
            },
            status_code=422,
        )

    crud.create_order(db, data)
    return RedirectResponse("/", status_code=303)


@router.get("/edit/{order_id}", response_class=HTMLResponse)
def edit_form(order_id: int, request: Request, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "order": order,
            "error": None,
        },
    )


@router.post("/edit/{order_id}")
def update_order(
    order_id: int,
    request: Request,
    order_number: str = Form(...),
    customer_name: str = Form(...),
    total_price: str = Form(...),
    order_date: str = Form(...),
    db: Session = Depends(get_db),
):
    form_data = {
        "id": order_id,
        "order_number": order_number,
        "customer_name": customer_name,
        "total_price": total_price,
        "order_date": order_date,
    }

    try:
        data = OrderCreate(**form_data)
    except ValidationError as exc:
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "order": form_data,
                "error": exc.errors()[0]["msg"],
            },
            status_code=422,
        )

    existing_order = crud.get_order_by_number(db, data.order_number)
    if existing_order and existing_order.id != order_id:
        return templates.TemplateResponse(
            "edit.html",
            {
                "request": request,
                "order": form_data,
                "error": "Order number already exists",
            },
            status_code=422,
        )

    crud.update_order(db, order_id, data)
    return RedirectResponse("/", status_code=303)


@router.get("/delete/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    crud.delete_order(db, order_id)
    return RedirectResponse("/", status_code=303)
