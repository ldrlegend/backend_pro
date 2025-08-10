from app.db.session import SessionLocal
from app.models import user, product

def insert_sample_data():
    db = SessionLocal()

    # Insert sample users
    user1 = user.User(name="John Doe", email="johndoe@example.com")
    user2 = user.User(name="Jane Smith", email="janesmith@example.com")

    db.add(user1)
    db.add(user2)

    db.commit()
    db.close()

    print("Sample data inserted!")

if __name__ == "__main__":
    insert_sample_data()
