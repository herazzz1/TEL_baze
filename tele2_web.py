from bs4 import BeautifulSoup
import requests

from tel_baze import Atsiskaitymas, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()

source = requests.get("https://tele2.lt/privatiems/mobilieji-telefonai").text
soup = BeautifulSoup(source, 'html.parser')
blokai = soup.find_all('div', class_="p1mkb7qa g1at0zcf item-type-narrow")

def pildau():
    for blokas in blokai:
        pavadinimas = blokas.find('div', class_="mmd8yt8").text.strip()
        modelis = blokas.find('div', class_="t1fy6h9g short").text
        kainos_blokas = blokas.find('div', class_="f50dtpa")
        #---- kaina gaunu su nuolaoda ir tikrą kaip vieną skaičių todėl atrenku kur su nuolaida ir išimu seną kainą iš naujos
        try:
            visa_kaina = kainos_blokas.find('span', class_="price has-old").text
            sena_kaina = kainos_blokas.find('span', class_="old-price").text
            kaina = visa_kaina.replace(sena_kaina,'')
        except:
            kaina = kainos_blokas.find('span', class_="price").text
        #--- kaina būna su kableliu, pakeičiu tipą į float, suapvalinu ir atiduodu integer
        kaina = kaina.replace('€','').strip()
        kaina = kaina.replace(',','.')
        kaina = round(float(kaina))
        kaina = int(kaina)
        telefonas = Atsiskaitymas(pavadinimas,modelis,kaina,"TELE2 ")
        session.add(telefonas)
    session.commit()
