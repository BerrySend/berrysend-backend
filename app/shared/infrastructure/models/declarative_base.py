from sqlalchemy.orm import DeclarativeBase

class ORMBase(DeclarativeBase):
    """
    Declarative base from SQLAlchemy (this won't create any table)
    """
    pass