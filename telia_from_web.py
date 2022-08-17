from bs4 import BeautifulSoup
import requests
import kainos_redagavimas as kr


from tel_baze import Atsiskaitymas, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = engine)
session = Session()
adresas = "https://www.telia.lt/prekes/mobilieji-telefonai?q=%3Arelevance&page="

def mobiliakai():
    for i in range(8):
        try:             #kolkas yra tik 5 puslapiai, todėl jei nebus daugiau tai pass
            source = requests.get(adresas+str(i)).text
            soup = BeautifulSoup(source, 'html.parser')
            blokai = soup.find_all('div', class_="col-lg-4 col-sm-6 col-xs-12")
            for blokas in blokai:
                    title = blokas.find('a', class_="mobiles-product-card__title js-open-product").text.strip()
                    price = blokas.find('div', class_="mobiles-product-card__full-price price").text.strip()
                    price = price.split('€')[0].strip().replace(' ', '')
                 #-------specialaus simbolio panaikinimas is didesnes kainos
                    kaina = kr.kaina_red(price)
                #------atskiriu pavadinimą ir modelį
                    modelis = title.split(' ')[0]
                    pavadinimas = title.replace(modelis, '').lstrip()
                    telefonas = Atsiskaitymas(modelis, pavadinimas, kaina, "TELIA ")
                    session.add(telefonas)
        except:
            pass
    session.commit()

