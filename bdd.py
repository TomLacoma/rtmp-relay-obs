import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



Base = declarative_base()


engine = None
session = None



class Flux(Base):
    __tablename__ = "flux"
    id = sqlalchemy.Column(sqlalchemy.BigInteger(), primary_key=True)
    in_flux = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
    out_flux = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
    infos = sqlalchemy.Column(sqlalchemy.String(1024), nullable=True)

engine = sqlalchemy.create_engine("mysql+pymysql://obsuser:cestvraimenthistoirededirequoi@localhost/obs")

# Création des tables si elles n'existent pas déjà
Base.metadata.create_all(engine)

# Ouverture de la session
Session = sessionmaker(bind=engine)
session = Session()
