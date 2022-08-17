import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

#--baze kuriame C diske
path ="C:\\Baze"
isExist = os.path.exists("C:\\Baze")
if not isExist:         #--tikrinu ar yra aplankas, jei ne sukuriu
    os.makedirs(path)
engine = create_engine('sqlite:///C:\\Baze\\telefonai.db')  #---tame aplanke sukuriu DB
Base = declarative_base()

class Atsiskaitymas(Base):
    __tablename__ = 'Atsiskaitymas'
    id = Column(Integer, primary_key=True)
    modelis = Column("modelis",String)
    pavadinimas = Column("pavadinimas",String)
    kaina = Column("kaina",Integer)
    parduotuve = Column("parduotuve",String)
    radimas = Column("Naujinimo data", DateTime, default=datetime.datetime.utcnow)

    def __init__(self, modelis, pavadinimas, kaina , parduotuve):
        self.modelis = modelis
        self.pavadinimas = pavadinimas
        self.kaina = kaina
        self.parduotuve = parduotuve

    def __repr__(self):
        return f"{self.id}{self.modelis} {self.pavadinimas} {self.kaina} {self.parduotuve} {self.radimas}"

Base.metadata.create_all(engine)