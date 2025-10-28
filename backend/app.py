import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from models import Base
import auth as auth_bp
import products as products_bp
import cart as cart_bp
import orders as orders_bp
import ai as ai_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, future=True)
    Base.metadata.create_all(engine)

    def get_session():
        return SessionLocal()

    app.session = get_session

    CORS(app, origins=app.config["CORS_ORIGINS"] or "*", supports_credentials=True)

    app.register_blueprint(auth_bp.bp)
    app.register_blueprint(products_bp.bp)
    app.register_blueprint(cart_bp.bp)
    app.register_blueprint(orders_bp.bp)
    app.register_blueprint(ai_bp.bp)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    @app.get("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config["BACKEND_PORT"]
    app.run(host="0.0.0.0", port=port, debug=app.config.get("FLASK_ENV") == "development")
