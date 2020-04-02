import os
import sqlalchemy as sa
from sqlalchemy.orm.session import sessionmaker

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('HOST')
db = os.environ.get('DB')
if user or password or host or db:
  import logging
  logging.warn('DB, DB_USER, DB_PASSWORD, and HOST are deprecated, please use DB_URI (mysql+pymysql://{USER}:{PASS}@{HOST}/{DB})')
db_uri = os.environ.get('DB_URI', 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(user, password, host, db))

engine = sa.create_engine(db_uri, pool_recycle=300)
Session = sessionmaker(bind=engine)

def init():
  from app.models import Base
  Base.metadata.create_all(engine)

def object_as_dict(obj):
  return {
    c.key: getattr(obj, c.key)
    for c in sa.inspect(obj).mapper.column_attrs
  }
