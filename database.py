from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DATABASE_URL = "postgresql://postgresql:03252009@localhost/fastproject"
engine=create_engine(DATABASE_URL)

Base=declarative_base()
SesionLocal=sessionmaker(autocommit=False,auto_refresh=False)
