from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from wiki_keep.Configuration import *

# DATABASE_URL = 'mysql://root:root@172.18.0.2:3306/WikiKeep'
DATABASE_URL = f"{db_name}://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_schema}"
engine = create_engine(DATABASE_URL,  pool_recycle=60)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)