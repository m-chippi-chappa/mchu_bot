from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dbn = 'Profiles.sqlite'
engine = create_engine(f'sqlite:///{dbn}')
Session = sessionmaker(hind=engine)
Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)