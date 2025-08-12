import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import SessionLocal
from app.models import user, product

def insert_sample_data():
    db = SessionLocal()

    # Clear existing data first
    db.query(product.Product).delete()
    db.query(user.User).delete()
    db.commit()
    print("Existing data cleared.")

    # Insert sample users
    user1 = user.User(name="John Doe", email="johndoe@example.com", role="user")
    user2 = user.User(name="Khánh Trần", email="khanhtran@gohub.com", role="admin")

    db.add(user1)
    db.add(user2)

    # Insert sample products
    product1 = product.Product(
        product_code="THADTF",
        status="active",
        type_of_sim="SIM",
        operator_code="DTAC",
        vendor_code="DTAC",
        purchase_type="API Purchase",
        sku_type="Base",
        data_type="Fixed Data",
        hotspot=True
    )
    product2 = product.Product(
        product_code="EUSAJYP",
        status="active",
        type_of_sim="eSIM",
        operator_code="JOYTEL",
        vendor_code="KANGO",
        purchase_type="API Purchase",
        sku_type="Base + Datapack",
        data_type="Daily Data",
        hotspot=False
    )

    db.add(product1)
    db.add(product2)

    db.commit()
    db.close()

    print("Sample data inserted!")

if __name__ == "__main__":
    insert_sample_data()
