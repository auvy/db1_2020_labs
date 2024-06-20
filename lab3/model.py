# import psycopg2
from sqlalchemy import create_engine, Column, String, Integer, BigInteger, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgres://postgres:qazpl,12345@localhost:5432/clothingStoreDatabase')
Base = declarative_base()


class Repr:
    def __repr__(self):
        clean_dict = self.__dict__.copy()
        clean_dict.pop('_sa_instance_state')
        return f'<{self.__class__.__name__}>{clean_dict})'


class Buyer(Base, Repr):
    __tablename__ = 'buyer'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)
    hashed_password = Column(String)
    city = Column(String)
    postal_code = Column(String)

    orders = relationship('Order')

    def __init__(self, email=None, name=None, hashed_password=None, city=None, postal_code=None ):
        self.email = email
        self.name = name
        self.hashed_password = hashed_password
        self.city = city
        self.postal_code = postal_code


class Order(Base, Repr):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    buyer_id = Column(Integer, ForeignKey('buyer.id'))

    order_items = relationship('OrderItem')

    def __init__(self, date=None, buyer_id=None):
        self.date = date
        self.buyer_id = buyer_id


class OrderItem(Base, Repr):
    __tablename__ = 'order_item'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    amount = Column(Integer)
    product_id = Column(Integer, ForeignKey('product.id'))

    def __init__(self, order_id=None, amount=None, product_id=None):
        self.order_id = order_id
        self.amount = amount
        self.product_id = product_id


class Product(Base, Repr):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    total_quantity = Column(Integer)

    order_items = relationship('OrderItem')

    def __init__(self, name=None, description=None, price=None, total_quantity=None):
        self.name = name
        self.description = description
        self.price = price
        self.total_quantity = total_quantity


session = sessionmaker(engine)()
Base.metadata.create_all(engine)

TABLES = {'buyer': Buyer, 'order': Order, 'order_item': OrderItem, 'product': Product}


class Model:
    def pairs_from_str(self, string):
        lines = string.split(',')
        pairs = {}
        for line in lines:
            key, value = line.split('=')
            pairs[key.strip()] = value.strip()
        return pairs

    def filter_by_pairs(self, objects, pairs, cls):
        for key, value in pairs.items():
            field = getattr(cls, key)
            objects = objects.filter(field == value)
        return objects

    def get(self, tname, condition):

        object_class = TABLES[tname]
        objects = session.query(object_class)

        if condition:
            try:
                pairs = self.pairs_from_str(condition)
            except Exception as err:
                raise Exception('Incorrect input')
            objects = self.filter_by_pairs(objects, pairs, object_class)

        return list(objects)

    def insert(self, tname, columns, values):
        columns = [c.strip() for c in columns.split(',')]
        values = [v.strip() for v in values.split(',')]

        pairs = dict(zip(columns, values))
        object_class = TABLES[tname]
        obj = object_class(**pairs)

        session.add(obj)

    def commit(self):
        session.commit()

    def delete(self, tname, condition):
        try:
            pairs = self.pairs_from_str(condition)
        except Exception as err:
            raise Exception('Incorrect input')
        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        objects.delete()

    def update(self, tname, condition, statement):
        try:
            pairs = self.pairs_from_str(condition)
            new_values = self.pairs_from_str(statement)
        except Exception as err:
            raise Exception('Incorrect input')

        object_class = TABLES[tname]

        objects = session.query(object_class)
        objects = self.filter_by_pairs(objects, pairs, object_class)

        for obj in objects:
            for field_name, value in new_values.items():
                setattr(obj, field_name, value)

    def fillProductByRandomData(self):
        sql = """
        CREATE OR REPLACE FUNCTION randomProducts()
            RETURNS void AS $$
        DECLARE
            step integer  := 0;
        BEGIN
            LOOP EXIT WHEN step > 1000;
                INSERT INTO product (name, description, price, total_quantity)
                VALUES (
                    substring(md5(random()::text), 1, 10),
                    substring(md5(random()::text), 1, 15),
                    (random() * (5000 - 1) + 1)::integer,
                    (random() * (7000 - 1) + 1)::integer
                );
                step := step + 1;
            END LOOP ;
        END;
        $$ LANGUAGE PLPGSQL;
        SELECT randomProducts();
        """
        try:
            session.execute(sql)
        finally:
            session.commit()
