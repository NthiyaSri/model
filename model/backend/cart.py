from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import CartAddSchema
from models import CartItem, Product
from utils import json_error, get_token_from_request, decode_jwt

bp = Blueprint("cart", __name__, url_prefix="/api/cart")


def require_user():
    token = get_token_from_request()
    if not token:
        return None, json_error("Unauthorized", 401)
    try:
        payload = decode_jwt(token, current_app.config["SECRET_KEY"])
        return payload, None
    except Exception:
        return None, json_error("Unauthorized", 401)


@bp.get("")
def get_cart():
    payload, err = require_user()
    if err:
        return err
    db: Session = current_app.session()
    items = db.scalars(select(CartItem).where(CartItem.user_id == payload["sub"])) .all()
    product_ids = [i.product_id for i in items]
    products = {p.id: p for p in db.scalars(select(Product).where(Product.id.in_(product_ids))).all()}
    return jsonify([
        {
            "id": i.id,
            "product": {
                "id": i.product_id,
                "title": products[i.product_id].title,
                "price": products[i.product_id].price,
                "image_url": products[i.product_id].image_url,
            },
            "quantity": i.quantity,
        }
        for i in items
    ])


@bp.post("")
def add_to_cart():
    payload, err = require_user()
    if err:
        return err
    data = request.get_json() or {}
    errors = CartAddSchema().validate(data)
    if errors:
        return json_error(errors, 400)
    db: Session = current_app.session()
    product = db.get(Product, data["product_id"])
    if not product:
        return json_error("Product not found", 404)
    existing = db.scalars(
        select(CartItem).where(CartItem.user_id == payload["sub"], CartItem.product_id == product.id)
    ).first()
    if existing:
        existing.quantity += data["quantity"]
    else:
        db.add(CartItem(user_id=payload["sub"], product_id=product.id, quantity=data["quantity"]))
    db.commit()
    return jsonify({"message": "added"})
