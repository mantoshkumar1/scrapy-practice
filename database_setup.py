from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from models import DeclarativeBase
from scrapers import settings

# Performs database connection using database settings from settings.py
# Variable type of engine: sqlalchemy engine
engine = create_engine(URL(**settings.DATABASE), echo=True)


def create_quotes_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


if __name__ == "__main__":
    create_quotes_table(engine)
