from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import CheckoutSchema
from models import CartItem, Order, OrderItem, Product
from utils import json_error, get_token_from_request, decode_jwt

bp = Blueprint("orders", __name__, url_prefix="/api")


def require_user():
    token = get_token_from_request()
    if not token:
        return None, json_error("Unauthorized", 401)
    try:
        payload = decode_jwt(token, current_app.config["SECRET_KEY"])
        return payload, None
    except Exception:
        return None, json_error("Unauthorized", 401)


@bp.post("/checkout")
def checkout():
    payload, err = require_user()
    if err:
        return err
    data = request.get_json() or {}
    errors = CheckoutSchema().validate(data)
    if errors:
        return json_error(errors, 400)

    db: Session = current_app.session()
    cart_items = db.scalars(select(CartItem).where(CartItem.user_id == payload["sub"])) .all()
    if not cart_items:
        return json_error("Cart is empty", 400)
    products = {
        p.id: p for p in db.scalars(select(Product).where(Product.id.in_([i.product_id for i in cart_items]))).all()
    }
    total = sum(products[i.product_id].price * i.quantity for i in cart_items)
    order = Order(user_id=payload["sub"], total=total, shipping_address=data["shipping_address"])
    db.add(order)
    db.flush()
    for item in cart_items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=products[item.product_id].price,
            )
        )
        db.delete(item)
    db.commit()
    return jsonify({"message": "order placed", "order_id": order.id, "total": total})
