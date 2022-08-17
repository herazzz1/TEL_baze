from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import sqlite3

from tel_baze import Atsiskaitymas, engine
from sqlalchemy.orm import sessionmaker

import paieskos_mygtukas as iesko
import visi_modeliai as rodo
import telia_from_web
import bite_web
import tele2_web
import senu_irasu_trinimas as salinam

#------ pagrindinė paleidimo funkcija

langas = Tk()
langas.iconbitmap(r'phone.ico')
langas.title("Telefonų kainų tikrinimo bazė")
#--- DB pridėjimas -----
Session = sessionmaker(bind=engine)
session = Session()

#---- funkcijos -----
def visas_sarasas():
    sarasas=[]
    telefonai = session.query(Atsiskaitymas).all()
    for i in telefonai:
        sarasas.append(f"{i.modelis} {i.pavadinimas} {i.parduotuve} {i.kaina} ")
    rodo.rodymas(sarasas)

def naujinu():
    err = 0
    dabar = datetime.utcnow() - timedelta(seconds=10)
    telefonas = session.query(Atsiskaitymas).first()
    if telefonas == None or (telefonas.radimas + timedelta(minutes=5) < dabar): #tikrina ar bazėje yra įrašas arba gal nesenai naujinta
        try:
            bite_web.pildau()
        except:
            messagebox.showerror("Error", "Bites nepavyko atnaujinti")
            err = err +1
        try:
            tele2_web.pildau()
        except:
            messagebox.showerror("Error", "Tele2 nepavyko atnaujinti")
            err = err + 1
        try:
            telia_from_web.mobiliakai()
        except:
            messagebox.showerror("Error", "Telia nepavyko atnaujinti")
            err = err + 1
        if err == 0:
            messagebox.showinfo("Atnaujinta", "DB sėkimingai atnaujinta")
            salinam.trinu(dabar)
    else:
        messagebox.showinfo("DB nesenai naujinta", "Bandykite naujinti po kelių minučių")
def iseiti():
    langas.quit()

meniu = Menu(langas)

langas.config(menu = meniu)
langas.geometry("300x200")
submeniu = Menu(meniu, tearoff=0)

#------lango meniu ir funkcijų kvietimas ------------
meniu.add_cascade(label="Atnaujinti sąrašą", command=naujinu)
meniu.add_cascade(label="Veiksmai", menu=submeniu)
submeniu.add_cascade(label="Paieška", command=iesko.paieskos_m)
submeniu.add_cascade(label="Visi telefonai", command=visas_sarasas)
submeniu.add_separator()
meniu.add_cascade(label="Išeiti", command=iseiti)


langas.mainloop()
