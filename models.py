from sqlalchemy import Column, Integer, String
from db import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    url = Column(String)
    category = Column(String)
    subcategory = Column(String)
    location = Column(String)
