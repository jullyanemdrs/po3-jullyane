from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine(
    "sqlite:///biblioteca.db",
    echo=False
)


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)
