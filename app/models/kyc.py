# from sqlalchemy import Column, Integer, String, Enum, Boolean, Text
# from sqlalchemy.sql import func
# from sqlalchemy.sql.sqltypes import TIMESTAMP
# from app.db.base import Base
# from sqlalchemy.orm import relationship

# class Boolean(Enum):
#     YES = "YES"
#     NO = "NO"

# class KYC(Base):
#     __tablename__ = "kyc"

#     id = Column(Integer, primary_key=True, index=True)
#     kyc_code = Column(Integer, unique=True, nullable=False, index=True)
#     kyc_needed= Column(Enum(Boolean), default=Boolean.NO)
#     kyc_link = Column(Text, nullable=True)
#     note = Column(Text, nullable=True)
#     date_created = Column(TIMESTAMP(timezone=True), server_default=func.now())
#     last_modified_date = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

#     products = relationship("Product", back_populates="kyc")

#     def __repr__(self):
#         return f"<KYC(id={self.id}, kyc_code='{self.kyc_code}', kyc_name='{self.kyc_name}')>"