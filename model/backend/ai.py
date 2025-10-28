from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Order, OrderItem, Product
from utils import get_token_from_request, decode_jwt

bp = Blueprint("ai", __name__, url_prefix="/api/ai")


def require_user_optional():
    token = get_token_from_request()
    if not token:
        return None
    try:
        payload = decode_jwt(token, current_app.config["SECRET_KEY"])
        return payload
    except Exception:
        return None


@bp.post("/description")
def ai_description():
    body = request.get_json() or {}
    title = body.get("title", "Product")
    features = body.get("features", [])
    short_desc = body.get("short_desc", "")
    # TODO: integrate real AI using current_app.config["AI_KEY"]
    description = f"{title}: {short_desc}. Highlights: " + (", ".join(features) if features else "great quality and value") + "."
    return jsonify({"description": description})


@bp.get("/recommendations")
def recommendations():
    payload = require_user_optional()
    db: Session = current_app.session()
    if payload:
        orders = db.scalars(select(Order).where(Order.user_id == payload["sub"])) .all()
        purchased_ids = set()
        for o in orders:
            for it in o.items:
                purchased_ids.add(it.product_id)
        prods = db.scalars(select(Product)).all()
        recs = [p for p in prods if p.id not in purchased_ids][:8]
    else:
        recs = db.scalars(select(Product).limit(8)).all()
    return jsonify([{"id": p.id, "title": p.title, "price": p.price, "image_url": p.image_url} for p in recs])
