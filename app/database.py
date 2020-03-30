import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('HOST')
db = os.environ.get('DB')
db_uri = os.environ.get('DB_URI', 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(user, password, host, db))

engine = create_engine(db_uri, pool_recycle=300)
Session = sessionmaker(bind=engine)

def init():
  from app.models import Base
  Base.metadata.create_all(engine)