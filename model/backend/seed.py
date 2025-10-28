import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
from models import Base, Category, Product, User

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)
Base.metadata.create_all(engine)


def main():
    db = SessionLocal()
    try:
        if not db.query(Category).first():
            cat_names = ["Electronics", "Books", "Fashion", "Home"]
            cats = [Category(name=n) for n in cat_names]
            db.add_all(cats)
            db.flush()
            prods = [
                Product(title="Wireless Headphones", short_desc="Noise-cancelling", price=99.99, category_id=cats[0].id, image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop"),
                Product(title="Smartphone", short_desc="128GB storage", price=499.00, category_id=cats[0].id, image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop"),
                Product(title="Sci-Fi Novel", short_desc="Bestseller", price=14.50, category_id=cats[1].id, image_url="https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop"),
                Product(title="Cotton T-Shirt", short_desc="Comfort fit", price=19.99, category_id=cats[2].id, image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop"),
                Product(title="Coffee Maker", short_desc="12-cup", price=39.99, category_id=cats[3].id, image_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop"),
            ]
            db.add_all(prods)
        else:
            # Update existing products with image URLs
            products = db.query(Product).all()
            image_urls = [
                "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop",  # Headphones
                "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop",  # Smartphone
                "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop",  # Book
                "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=300&fit=crop",  # T-Shirt
                "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&h=300&fit=crop",  # Coffee Maker
            ]
            for i, product in enumerate(products):
                if i < len(image_urls) and not product.image_url:
                    product.image_url = image_urls[i]
        
        if not db.query(User).filter_by(email="admin@example.com").first():
            db.add(User(email="admin@example.com", password_hash=pbkdf2_sha256.hash("admin123"), name="Admin", is_admin=True))
        db.commit()
        print("Seeded database.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
