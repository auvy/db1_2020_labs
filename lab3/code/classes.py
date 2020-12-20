from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

class Repr:
    def __repr__(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        return f'<{self.__class__.__name__}>{clean_dict})'

class Route(Base, Repr):
    __tablename__ = 'routes'

    id = Column(Integer, primary_key=True)
    departId = Column(Integer, ForeignKey('station.id'))
    arriveId = Column(Integer, ForeignKey('station.id'))
    lastId = Column(Integer, ForeignKey('station.id'))
    departTime = Column(Date)
    arriveTime = Column(Date)
    trainId = Column(Integer, ForeignKey('train.id'))

    def __init__(self, departId=None, arriveId=None, lastId=None, departTime=None, arriveTime=None, trainId=None ):
        self.departId = departId
        self.arriveId = arriveId
        self.lastId = lastId
        self.departTime = departTime
        self.arriveTime = arriveTime
        self.trainId = trainId
    
class Station(Base, Repr):
    __tablename__ = 'routes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    availability = Column(Boolean)

    def __init__(self, name=None, availability=None ):
        self.name = name
        self.availability = availability


class Train(Base, Repr):
    __tablename__ = 'routes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tType = Column(String)

    def __init__(self, name=None, tType=None ):
        self.name = name
        self.tType = tType


class Wagon(Base, Repr):
    __tablename__ = 'routes'
    
    id = Column(Integer, primary_key=True)
    trainId = Column(Integer, ForeignKey('train.id'))
    subType = Column(String)
    number = Column(Integer)

    def __init__(self, trainId=None, subType=None, number=None):
        self.trainId = trainId
        self.subType = subType
        self.number = number



session = sessionmaker(engine)()
Base.metadata.create_all(engine)

TABLES = {'buyer': Buyer, 'order': Order, 'order_item': OrderItem, 'product': Product}
