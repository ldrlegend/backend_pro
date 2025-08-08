from app.db.session import engine
from app.db.base import Base
from app.models import user, product  # import các models để chúng được "đăng ký"

def init_db():
    Base.metadata.create_all(bind=engine)
    