'''just an attempt for starters'''

from day_data import *
from year_data import *

from tkinter import *
from tkinter.ttk import Combobox
import matplotlib.pyplot as plt
from numpy import size
from tkcalendar import *


class Application(Tk): 

    def func(self): 

        self.new_path = self.data.get()
        energy_per_year(self.new_path)

    def func1(self): 

        text = str(self.button.get_date())
        t = text.split("-")
        self.new_path = t[0] + t[1] + t[2]
        energy_per_day(self.new_path)

    def makeSourceButton(self): 

        self.button.destroy()

        self.data.set("Pick a source")

        options = ["Time", "Solar", "Wind", "Geothermal", "Biomass", "Biogas", "Small hydro", "Coal", "Nuclear", "Natural gas", "Large hydro", "Batteries", "Imports", "Other"]
        self.button = OptionMenu(self.dataButtonCanvas, self.data, *options)
        self.button.grid(row = 0, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func)
        self.goButton.grid(row = 0, column = 1)

    def makeYearButton(self): 

        self.button.destroy()

        self.data.set("Pick a year")

        options = ["2019", "2020", "2021"]
        self.button = OptionMenu(self.dataButtonCanvas, self.data, *options)
        self.button.grid(row = 0, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func)
        self.goButton.grid(row = 0, column = 1)

    def makeDateButton(self): 

        self.button.destroy()

        self.data.set("Pick a date")

        self.button = DateEntry(self.dataButtonCanvas, width= 16, highlightbackground = 'pink', background= "magenta3", foreground= "white",bd=0)
        self.button.grid(row = 0, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func1)
        self.goButton.grid(row = 0, column = 1)

    def makeButtons(self, xaxisCanvas): 

        self.clicked = BooleanVar()
        self.data = StringVar()
        self.new_path = ""
        self.button = Button()

        button1 = Button(xaxisCanvas, width = 10, text = 'By year', font = 'sans-serif', command = self.makeYearButton)
        button1.grid(row = 0, column = 0, sticky = 'w', padx = (0, 30))

        button2 = Button(xaxisCanvas, width = 10, text = "By day", font = 'sans-serif', command =  self.makeDateButton)
        button2.grid(row = 0, column = 1)

        button3 = Button(xaxisCanvas, width = 10, text = "By source", font = 'sans-serif', command = self.makeSourceButton)
        button3.grid(row = 0, column = 2, sticky = 'e', padx = (30, 0))

        self.dataButtonCanvas = Canvas(self, height = 150, background = 'pink', highlightbackground = 'pink') 
        self.dataButtonCanvas.grid(row = 2, columnspan = 3, sticky = "n")

    def makeXAxisCanvas(self): 

        xaxisCanvas = Canvas(self, background = 'pink', highlightbackground = 'pink', height = 150)
        xaxisCanvas.grid(row = 1, column= 0, sticky = "n")
        xaxisCanvas.columnconfigure(0, weight = 1)
        xaxisCanvas.columnconfigure(1, weight = 1)
        xaxisCanvas.columnconfigure(2, weight = 1)
        self.makeButtons(xaxisCanvas)

    def makeLabelCanvas(self): 

        labelCanvas = Canvas(self, height = 150, background = 'pink', highlightbackground = 'pink')
        labelCanvas.grid(row = 0, column= 0)

        label = Label(labelCanvas, text = "Pick type of graph", background = 'pink', font = ('sans-serif', 20))
        label.grid(row = 0, column = 0)

    def __init__(self):
        super().__init__()
        self.geometry("500x300+700+400")
        self.resizable(False, False)
        self.title("an attempt")
        self.configure(bg = 'pink')
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.makeLabelCanvas()
        self.makeXAxisCanvas()

app = Application()
app.mainloop()
