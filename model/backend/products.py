from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, and_
from models import Product
from schemas import ProductCreateSchema
from utils import json_error, get_token_from_request, decode_jwt

bp = Blueprint("products", __name__, url_prefix="/api/products")


def require_admin():
    token = get_token_from_request()
    if not token:
        return None, json_error("Unauthorized", 401)
    try:
        payload = decode_jwt(token, current_app.config["SECRET_KEY"])
        if not payload.get("is_admin"):
            return None, json_error("Forbidden", 403)
        return payload, None
    except Exception:
        return None, json_error("Unauthorized", 401)


@bp.get("")
def list_products():
    db: Session = current_app.session()
    q = request.args.get("q", "").strip()
    category = request.args.get("category")
    page = int(request.args.get("page", "1"))
    limit = int(request.args.get("limit", "12"))
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    stmt = select(Product)
    conditions = []
    if q:
        like = f"%{q.lower()}%"
        conditions.append(or_(Product.title.ilike(like), Product.short_desc.ilike(like), Product.description.ilike(like)))
    if category:
        try:
            category_id = int(category)
            conditions.append(Product.category_id == category_id)
        except ValueError:
            pass
    if min_price:
        try:
            conditions.append(Product.price >= float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            conditions.append(Product.price <= float(max_price))
        except ValueError:
            pass
    if conditions:
        stmt = stmt.where(and_(*conditions))

    items = db.scalars(stmt.offset((page - 1) * limit).limit(limit)).all()
    return jsonify([
        {"id": p.id, "title": p.title, "short_desc": p.short_desc, "price": p.price, "image_url": p.image_url, "category_id": p.category_id}
        for p in items
    ])


@bp.get("/<int:pid>")
def get_product(pid: int):
    db: Session = current_app.session()
    p = db.get(Product, pid)
    if not p:
        return json_error("Not found", 404)
    return jsonify({
        "id": p.id, "title": p.title, "short_desc": p.short_desc, "description": p.description,
        "price": p.price, "image_url": p.image_url, "category_id": p.category_id
    })


@bp.post("")
def create_product():
    payload, err = require_admin()
    if err:
        return err
    db: Session = current_app.session()
    data = request.get_json() or {}
    errors = ProductCreateSchema().validate(data)
    if errors:
        return json_error(errors, 400)
    product = Product(**data)
    db.add(product)
    db.commit()
    return jsonify({"id": product.id}), 201


@bp.put("/<int:pid>")
def update_product(pid: int):
    payload, err = require_admin()
    if err:
        return err
    db: Session = current_app.session()
    p = db.get(Product, pid)
    if not p:
        return json_error("Not found", 404)
    data = request.get_json() or {}
    for k in ["title", "short_desc", "description", "price", "image_url", "category_id"]:
        if k in data:
            setattr(p, k, data[k])
    db.commit()
    return jsonify({"message": "updated"})


@bp.delete("/<int:pid>")
def delete_product(pid: int):
    payload, err = require_admin()
    if err:
        return err
    db: Session = current_app.session()
    p = db.get(Product, pid)
    if not p:
        return json_error("Not found", 404)
    db.delete(p)
    db.commit()
    return jsonify({"message": "deleted"})
