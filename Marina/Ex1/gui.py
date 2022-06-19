from day_data import *
from year_data import *

from tkinter import *
from tkcalendar import *

class Application(Tk): 

    def yearBtnFunc(self): 
        '''Calls functions to create graph for specified year'''
        
        self.new_path = self.data.get()
        self.new_path = int(self.new_path)
        energy_per_year(self.new_path)

    def dateBtnFunc(self): 
        '''Calls functions to create graph for specified date '''

        text = str(self.button.get_date())
        t = text.split("-")
        self.year = int(t[0])
        self.month = int(t[1])
        self.day = int(t[2])
        energy_per_day(self.year, self.month, self.day)

    def makeYearButton(self): 
        '''Makes year selection button and go button that calls function to create graph'''

        self.button.destroy()
        self.data.set("Pick a year")

        options = ["2019", "2020", "2021"]
        self.button = OptionMenu(self.dataButtonCanvas, self.data, *options)
        self.button.grid(row = 0, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.yearBtnFunc)
        self.goButton.grid(row = 0, column = 1)

    def makeDateButton(self): 
        '''Makes date selection button and go button that calls function to create graph'''

        self.button.destroy()

        self.button = DateEntry(self.dataButtonCanvas, width= 16, highlightbackground = 'pink', background= "magenta3", foreground= "white",bd=0)
        self.button.grid(row = 0, column = 0)

        self.goButton = Button(self.dataButtonCanvas, text = "Go", font = 'sans-serif', command = self.dateBtnFunc)
        self.goButton.grid(row = 0, column = 1)

    def makeButtons(self, xaxisCanvas): 
        '''Makes selection buttons for the type of graph'''

        self.clicked = BooleanVar()
        self.data = StringVar()
        self.button = Button() #appears after type of graph is selected, destroyed if another type gets selected afterwards

        button1 = Button(xaxisCanvas, width = 10, text = 'By year', font = 'sans-serif', command = self.makeYearButton)
        button1.grid(row = 0, column = 0, sticky = 'w', padx = (0, 30))

        button2 = Button(xaxisCanvas, width = 10, text = "By day", font = 'sans-serif', command =  self.makeDateButton)
        button2.grid(row = 0, column = 1)

        self.dataButtonCanvas = Canvas(self, height = 150, background = 'pink', highlightbackground = 'pink') 
        self.dataButtonCanvas.grid(row = 2, columnspan = 3, sticky = "n")

    def makeXAxisCanvas(self): 
        '''Makes canvas inside which selection buttons are placed to decide on the time duration of the graph info'''

        xaxisCanvas = Canvas(self, background = 'pink', highlightbackground = 'pink', height = 150)
        xaxisCanvas.grid(row = 1, column= 0, sticky = "n")
        xaxisCanvas.columnconfigure(0, weight = 1)
        xaxisCanvas.columnconfigure(1, weight = 1)
        self.makeButtons(xaxisCanvas)

    def makeLabelCanvas(self): 
        '''Makes a canvas instance inside which to place info label'''

        labelCanvas = Canvas(self, height = 150, background = 'pink', highlightbackground = 'pink') #canvas
        labelCanvas.grid(row = 0, column= 0)

        label = Label(labelCanvas, text = "Pick type of graph", background = 'pink', font = ('sans-serif', 20)) #label
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