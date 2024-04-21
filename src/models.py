from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from clickhouse_sqlalchemy import engines
Base = declarative_base()

from sqlalchemy import create_engine, DDL
from sqlalchemy.orm import sessionmaker
conn_str = 'clickhouse://default:@localhost/default'
engine = create_engine(conn_str)
session = sessionmaker(bind=engine)()

database = 'test'


def create_database(engine):
    print('createing DB')
    engine.execute(DDL(f'CREATE DATABASE IF NOT EXISTS {database}'))


class NewTable(Base):
    __tablename__ = 'new_table'
    __table_args__ = (
        engines.MergeTree(order_by=['id']),
        {'schema': database},
    )
    id = Column(Integer, primary_key=True)
    var1 = Column(String)
    var2 = Column(String)


def create_table(engine):
    NewTable.__table__.create(engine)
