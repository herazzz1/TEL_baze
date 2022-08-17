from tkinter import *

import visi_modeliai as rodo

from tel_baze import Atsiskaitymas, engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()


class paieskos_m:
    def __init__(self):
        self.err = False
        self.modelio_ivedimas = Label(text="Iveskite ieškomą modelį")
        self.modelis = Entry(background="Yellow")
        self.pavadinimo_ivedimas = Label(text="Iveskite ieškomą pavadinimą")
        self.pavadinimas = Entry(background="Yellow")
        self.maz_k_ivedimas = Label(text="Mažiausia kaina")
        self.maz_k = Entry(background="Green")
        self.did_k_ivedimas = Label(text="Didžiausia kaina")
        self.did_k = Entry(background="Orange")
        self.ieskoti_m = Button(text="Ieškoti", command=self.onClick)
        self.iseiti = Button(text="Išeiti", command=self.uzdarau)
        self.modelio_ivedimas.grid(row=0, column=0)
        self.pavadinimo_ivedimas.grid(row=1, column=0)
        self.modelis.grid(row=0, column=1)
        self.pavadinimas.grid(row=1, column=1)
        self.maz_k_ivedimas.grid(row=2, column=0)
        self.maz_k.grid(row=2, column=1)
        self.did_k_ivedimas.grid(row=3, column=0)
        self.did_k.grid(row=3,column=1)
        self.ieskoti_m.grid(row=5, column=1)
        self.iseiti.grid(row=5, column=0)
        self.ieskoti_m.bind("<Return>", self.onClick)
        self.iseiti.bind("<Return>",self.uzdarau)
    def onClick(self):
        sarasas = []
        telefonai = session.query(Atsiskaitymas).all()
        modelis = self.modelis.get()
        pavadinimas = self.pavadinimas.get()
        maz_k = self.maz_k.get()
        did_k = self.did_k.get()
        #---paieška pagal įvestus kriterijus----
        if (modelis or pavadinimas) and (maz_k or did_k):
            try:
                if maz_k:
                    maz_k = int(maz_k)
                else:
                    maz_k = 0
                if did_k:
                    did_k = int(did_k)
                else:
                    did_k = 9999
                for i in telefonai:
                    if i.kaina > maz_k and i.kaina < did_k and (i.modelis.upper() == modelis.upper() or pavadinimas.upper() in i.pavadinimas.upper()):
                        sarasas.append(f"{i.modelis} {i.pavadinimas} {i.parduotuve.upper()} {i.kaina} ")
            except:
                self.klaida = Label(text="Kainoje veskite tik skaičius")
                self.klaida.grid(row=4, column=1)
                self.err = True
        elif modelis:
            for i in telefonai:
                if modelis.upper() == i.modelis.upper():
                    sarasas.append(f"{i.modelis} {i.pavadinimas} {i.parduotuve} {i.kaina} ")
        elif pavadinimas:
            for i in telefonai:
                if pavadinimas.upper() in i.pavadinimas.upper():
                    sarasas.append(f"{i.modelis} {i.pavadinimas} {i.parduotuve} {i.kaina} ")
        elif maz_k or did_k:
            try:
                if maz_k:
                    maz_k = int(maz_k)
                else:
                    maz_k = 0
                if did_k:
                    did_k = int(did_k)
                else:
                    did_k = 9999
                for i in telefonai:
                    if i.kaina > maz_k and i.kaina < did_k:
                        sarasas.append(f"{i.modelis} {i.pavadinimas} {i.parduotuve} {i.kaina} ")
            except:
                self.klaida = Label(text="Kainoje veskite tik skaičius")
                self.klaida.grid(row=4, column=1)
                self.err = True
        else:
            return False
        sarasas.sort()
        rodo.rodymas(sarasas)

    def uzdarau(self):
        self.modelio_ivedimas.destroy()
        self.pavadinimo_ivedimas.destroy()
        self.modelis.destroy()
        self.pavadinimas.destroy()
        self.ieskoti_m.destroy()
        self.iseiti.destroy()
        self.maz_k.destroy()
        self.did_k.destroy()
        self.maz_k_ivedimas.destroy()
        self.did_k_ivedimas.destroy()
        if self.err:
            self.klaida.destroy()
