from tkinter import *

class rodymas:
    def __init__(self, telefonai):
        self.telefonai = telefonai
        self.langas_s = Tk()
        self.langas_s.geometry("600x400")
        scrollbar = Scrollbar(self.langas_s)
        scrollbar.grid(row=1,column=2, sticky='ns')
        tekstas = Label(self.langas_s, text="Visi skirtingi modeliai")
        boksas = Listbox(self.langas_s, height=20, width=70, yscrollcommand = scrollbar.set)
        nr = 1
        for line in self.telefonai:
            boksas.insert(END,f"{nr} {line}")
            nr = nr+1
        tekstas.grid(row=0, column=0)
        boksas.grid(row=1, column=1)
        scrollbar.config(command=boksas.yview)
        self.mygtukas = Button(self.langas_s, text="uždaryti", command=self.onClick)
        self.mygtukas.grid(row=2, column=1)
    def onClick(self):
        self.langas_s.destroy()
