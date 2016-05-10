from sqlalchemy import (
    create_engine, Column, Integer, String, Numeric,
    DateTime, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# will change to whatever I need for RDS at deployment time
engine = create_engine('sqlite:///requests.db')
Session = sessionmaker(bind=engine)

class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True)
    lat_lon = Column(Numeric) # maybe rounded for privacy
    n_taco_bells = Column(Integer)
    desired_distance = Column(Numeric)

class Result(Base):
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    nearest_taco_bell_id = Column(String)
    route_id = Column(String)
    route_url = Column(String)

    @classmethod
    def add(cls, nearest_taco_bell_id):
        sess = Session()
        if (
                sess
                .query(cls.nearest_taco_bell_id == nearest_taco_bell_id)
                .count()
        ) == 0:
            # go get the route from google maps, add all that info to db
            pass

