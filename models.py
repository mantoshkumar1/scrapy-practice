from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

DeclarativeBase = declarative_base()


class Author(DeclarativeBase):
    """Sqlalchemy Author model
    An author can write multiple quotes
    """
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    author_url = Column('author_url', String, nullable=True)
    quotes = relationship("Quotes")
    __table_args__ = (
        UniqueConstraint("name", name="_author_name_unique"),
    )


class Quotes(DeclarativeBase):
    """Sqlalchemy quotes model
    A particular quote can be written by only one author.
    A particular author can write multiple quotes.
    """
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True)
    content = Column('content', String, nullable=False)
    tags = Column('tags', String, nullable=True)
    author_id = Column(Integer, ForeignKey('author.id'))
