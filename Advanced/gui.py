import sys 
import os
from data_analysis.graphics.day_data import *
from data_analysis.graphics.year_data import *
from data_analysis.graphics.source_data import *
from data_analysis.graphics.outlier_finder import *
from data_analysis.graphics.import_data import *
from data_analysis.graphics.functions import *
from data_analysis.path import *
from tkinter import *
from tkcalendar import *
import pandas as pd

real_path = os.path.realpath(__file__)
real_path = resolve_path(real_path)
dir_path = os.path.dirname(real_path)

sys.path.append(dir_path)
data_path = "{}\data".format(dir_path)
os.chdir(data_path)
df = pd.read_csv("merged_files.csv")

from zipfile import ZipFile

if os.path.exists("processed_demands.zip"):
    with ZipFile('processed_demands.zip', 'r') as zipObj:
    # Extract all the contents of zip file in current directory
        zipObj.extractall()
    os.remove("processed_demands.zip")

os.chdir(dir_path)

import neural_network
from neural_network.RestAPI import *

class Application(Tk): 

    def func(self): 
        '''Calls function to create graph for specified year'''
        
        self.new_path = self.data.get()
        self.new_path = int(self.new_path)
        energy_per_year(self.new_path)

    def func1(self): 
        '''Calls function to create graph for specified date '''

        text = str(self.button.get_date())
        t = text.split("-")
        self.year = int(t[0])
        self.month = int(t[1])
        self.day = int(t[2])
        energy_per_day(self.year, self.month, self.day)

    def func2(self): 
        '''Calls function to create graph for specified source'''

        options = ["Solar", "Wind", "Geothermal", "Biomass", "Biogas", "Small hydro", "Coal", "Nuclear", "Natural gas", "Large hydro", "Batteries", "Imports", "Other"]
        source = self.data.get()
        index = options.index(source)
        self.new_path = index
        source_per_day(self.new_path)
    
    def func3(self):
        '''Calls function to create graph of days and find outliers'''

        data = [self.entry1.get(),self.entry2.get()]
        counter=0
        data_new=[]
        for i in range(len(data)):
            result=checkTime(data[i])
            if result==None:counter+=1
            else:
                data_new.append(int(result[0:2]))
        if counter>0:
            print("Wrong input")
        elif (len(data_new)==2 and data_new[0]>data_new[1]):
            print("End Time must be bigger than Start Time")
        else:
            self.new_path = data_new
            find_outliers(self.new_path)

    def func4(self):
        '''Calls function to open web app after closing GUI window'''

        self.destroy()
        app = create_app()
        app.run()

    def func5(self):
        '''Calls function to import new data'''
        
        data = self.e3.get()
        res = checkFileName(data)
        print(res)
        if res==None or res=="WrongDate":
            print("Wrong Input")
        else:
            self.new_path = data
            insertfiles(data)
        
    def makeOutlierButton(self):
        '''Enables outlier button on GUI'''

        if(len(self.dataButtonCanvas.winfo_children())>0):
            for item in self.dataButtonCanvas.winfo_children():
                item.destroy()

        self.data.set("Pick outlier search hours(entries have to be type of xx:00)")
        print("Get Outliers")

        self.Label1 = Label(self.dataButtonCanvas,text="Inster start hour(xx:00)",background = 'pink').grid(row=1,column=1)
        self.entry1= Entry(self.dataButtonCanvas)
        self.entry1.grid(row=2,column=1)
        self.Label2 = Label(self.dataButtonCanvas,text="Insert end hour(xx:00)",background = 'pink').grid(row=1,column=2)
        self.entry2= Entry(self.dataButtonCanvas)
        self.entry2.grid(row=2,column=2)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func3) #button that calls respective function for action
        self.goButton.grid(row = 2, column = 3)
    
    def makeImportButton(self):
        '''Enables button for file import'''

        if(len(self.dataButtonCanvas.winfo_children())>0):
            for item in self.dataButtonCanvas.winfo_children():
                item.destroy()
        print("Import Data File")

        self.Label1 = Label(self.dataButtonCanvas,text="Name of file (the name must be a date for example (20220202) and must be a csv file)",background = 'pink').grid(row=1,column=1)
        self.e3= Entry(self.dataButtonCanvas)
        self.e3.grid(row=2,column=1)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func5) #button that calls respective function for action
        self.goButton.grid(row = 3, column = 1)

    def makeSourceButton(self): 
        '''Enables button for source graphic'''

        if(len(self.dataButtonCanvas.winfo_children())>0):
            for item in self.dataButtonCanvas.winfo_children():
                item.destroy()
        print("Get Graph by Source")
        self.data.set("Pick a source")

        options = ["Solar", "Wind", "Geothermal", "Biomass", "Biogas", "Small hydro", "Coal", "Nuclear", "Natural gas", "Large hydro", "Batteries", "Imports", "Other"]
        self.button = OptionMenu(self.dataButtonCanvas, self.data, *options)
        self.button.grid(row = 2, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func2) #button that calls respective function for action
        self.goButton.grid(row = 2, column = 1)

    def makeYearButton(self): 
        '''Enables button for energy graphic by yeah'''

        if(len(self.dataButtonCanvas.winfo_children())>0):
            for item in self.dataButtonCanvas.winfo_children():
                item.destroy()

        print("Get Graph by year")
        self.data.set("Pick a year")

        options = Years(df) #list of years available for graphic

        self.button = OptionMenu(self.dataButtonCanvas, self.data, *options)
        self.button.grid(row = 2, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func) #button that calls respective function for action
        self.goButton.grid(row = 2, column = 1)

    def makeDateButton(self): 
        '''Enables button for energy graphic by day'''
        if(len(self.dataButtonCanvas.winfo_children())>0):
            for item in self.dataButtonCanvas.winfo_children():
                item.destroy()

        print("Get Graph of energy by date")
        self.data.set("Pick a date")

        self.button = DateEntry(self.dataButtonCanvas, width= 16, highlightbackground = 'pink', background= "magenta3", foreground= "white",bd=0)
        self.button.grid(row = 2, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.func1) #button that calls respective function for action
        self.goButton.grid(row = 2, column = 1)

    def makeButtons(self, xaxisCanvas): 
        '''Creates GUI buttons'''

        self.clicked = BooleanVar()
        self.data = StringVar()
        self.new_path = ""
        self.button = Button()

        button1 = Button(xaxisCanvas, width = 10, text = 'By year', font = 'sans-serif', command = self.makeYearButton)
        button1.grid(row = 0, column = 0, sticky = 'w', padx = (0, 20))

        button2 = Button(xaxisCanvas, width = 10, text = "By day", font = 'sans-serif', command =  self.makeDateButton)
        button2.grid(row = 0, column = 1)

        button3 = Button(xaxisCanvas, width = 10, text = "By source", font = 'sans-serif', command = self.makeSourceButton)
        button3.grid(row = 0, column = 2, sticky = 'e', padx = (30, 0))
        
        label = Label(xaxisCanvas, text = "Modes", background = 'pink', font = ('sans-serif', 20))
        label.grid(row = 3, column = 1)

        button4 = Button(xaxisCanvas, width = 10, text = 'Outlier finder', font = 'sans-serif', command = self.makeOutlierButton)
        button4.grid(row = 4, column = 0, sticky = 'w', padx = (0, 30))

        button5 = Button(xaxisCanvas, width = 15, text = "Predictor", font = 'sans-serif', command =self.func4) #calls function to open web app 
        button5.grid(row = 4, column = 1)

        button6 = Button(xaxisCanvas, width = 10, text = "Import data", font = 'sans-serif', command = self.makeImportButton)
        button6.grid(row = 4, column = 2, sticky = 'e', padx = (30, 0))

        self.dataButtonCanvas = Canvas(self, height = 50, background = 'pink', highlightbackground = 'pink') 
        self.dataButtonCanvas.grid(row = 2, columnspan = 3, sticky = "n")
    
    def makeXAxisCanvas(self): 
        '''Canvas for operation buttons'''

        xaxisCanvas = Canvas(self, background = 'pink', highlightbackground = 'pink', height = 150)
        xaxisCanvas.grid(row = 1, column= 0, sticky = "n")
        xaxisCanvas.columnconfigure(0, weight = 1)
        xaxisCanvas.columnconfigure(1, weight = 1)
        xaxisCanvas.columnconfigure(2, weight = 1)
        self.makeButtons(xaxisCanvas)
    
    def makeXAxisCanvas1(self): 
        '''Canvas for operation buttons'''

        xaxisCanvas = Canvas(self, background = 'pink', highlightbackground = 'pink', height = 150)
        xaxisCanvas.grid(row = 4, column= 0, sticky = "n")
        xaxisCanvas.columnconfigure(0, weight = 1)
        xaxisCanvas.columnconfigure(1, weight = 1)
        xaxisCanvas.columnconfigure(2, weight = 1)
        self.makeButtons1(xaxisCanvas)
    
    def makeLabelCanvas(self): 
        '''Makes canvaces for labels on GUI'''

        labelCanvas = Canvas(self, height = 150, background = 'pink', highlightbackground = 'pink')
        labelCanvas.grid(row = 0, column= 0)

        label = Label(labelCanvas, text = "Pick type of graph", background = 'pink', font = ('sans-serif', 20))
        label.grid(row = 0, column = 0)
    
    def __init__(self):
        '''Creates window'''

        super().__init__()
        self.geometry("500x300+700+300")
        self.resizable(False, False)
        self.title("Energy Data")
        self.configure(bg = 'pink')
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(0, weight = 1)
        self.makeLabelCanvas()
        self.makeXAxisCanvas()

app = Application()
app.mainloop()