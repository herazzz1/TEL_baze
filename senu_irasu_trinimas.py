from tel_baze import Atsiskaitymas, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def trinu(nauja_data):
    telefonai = session.query(Atsiskaitymas).all()
    for i in telefonai:
        if i.radimas < nauja_data:
            session.delete(i)
    session.commit()
