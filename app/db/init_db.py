from app.db.session import engine
from app.db.base import Base
from app.models import user, product, vendor, operator, country, attribute, attribute_option, product_attribute_value_index, attribute_group # import các models để chúng được "đăng ký"

def init_db():
    Base.metadata.create_all(bind=engine)
    