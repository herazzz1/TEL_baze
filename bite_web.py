from bs4 import BeautifulSoup
import requests
import kainos_redagavimas as kr

from tel_baze import Atsiskaitymas, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

source = requests.get("https://www.bite.lt/telefonai#!filters/tags/issiuntimas-ta-pacia-diena").text
soup = BeautifulSoup(source, 'html.parser')
blokai = soup.find_all('div', class_="col-lg-4 col-6")

def pildau():
    for blokas in blokai:
        pavadinimas = blokas.find('h3', class_="product__pretitle").text.strip()
        modelis = blokas.find('h3', class_="product__title").text
        kaina = blokas.find('div', class_="product__price product__price--general").text
        price = kaina.split('€')[0].strip().replace(' ', '')
        kaina = kr.kaina_red(price)
        # print(kaina)
        if "Atidaryta pakuotė" in modelis:
            pass
        else:
            modelis = modelis.replace('išmanusis','').strip()
            modelis = modelis.replace('telefonas', '').strip()
            modelis = modelis.replace('mobilusis', '').strip()
            # print(modelis, kaina)
            # print(pavadinimas,modelis,kaina,)
            #---be atidarytų pakuočių
            telefonas = Atsiskaitymas(pavadinimas,modelis,kaina,"BITЕ ")
            session.add(telefonas)
    session.commit()