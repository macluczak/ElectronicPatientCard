from statistics import median
import tkinter as tk
from turtle import width
from fhirpy import AsyncFHIRClient
from pyparsing import col
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

class Info(tk.Frame):
    def __init__(self, parent, client, patient):
        tk.Frame.__init__(self, parent)
        self.client = client
        self.parent = parent
        self.patient = patient.pop()
        self.patientID = 'Patient/' +str(self.patient["id"])
        self.observationToDateDict  = {}
        self.observations = []
        self.getMedicalData()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.clicked = tk.StringVar(self)
        self.months = list(self.observationToDateDict.keys())
        self.clicked.set(self.months[0])




        

        self.backButton = tk.Button(self, text="BACK", command=self.back)
        self.title = tk.Label(self, text="PATIENT INFO", font=('Helvetica bold', 40))
        self.patientNameLabel = tk.Label(self, text="", font=("Helvetica", 15))
        self.patientBirthDateLabel = tk.Label(self, text="", font=("Helvetica", 15))
        self.patientGenderLabel = tk.Label(self, text="", font=("Helvetica", 15))
        self.patientIDLabel = tk.Label(self, text="", font=("Helvetica", 15))
        self.dropDownMonths = tk.OptionMenu(self, self.clicked, *self.months)
        self.selectMonthButton =  tk.Button(self, text="SELECT MONTH", command= self.clearAndFillNewMonth)
        self.scrollbarListbox = tk.Scrollbar(self, orient='vertical')
        self.detailsListbox = tk.Listbox(self,width=50, height= 5, yscrollcommand= self.scrollbarListbox.set)
        self.fillListBox(self.observationToDateDict[self.months[0]])

        self.scrollbarListbox.config(command=self.detailsListbox.yview)

   
        self.patientFullname = "PATIENT NAME: " + str(self.patient["name"][0].given[0]) + " " + str(self.patient["name"][0].family)
        self.patiendBirthDateText = " BIRTH DATE: " + str(self.patient["birthDate"])
        self.patientGenderText = " GENDER: " + str(self.patient["gender"])
        self.patientIDText = " ID: " + str(self.patient["id"])

        self.patientNameLabel['text'] = self.patientFullname
        self.patientBirthDateLabel['text'] = self.patiendBirthDateText
        self.patientGenderLabel['text'] = self.patientGenderText
        self.patientIDLabel['text'] = self.patientIDText
        

        self.title.grid(row=0, column=0, columnspan=2)

        self.patientNameLabel.grid(row=1, column=0, columnspan=2)

        self.patientBirthDateLabel.grid(row=2, column=0, columnspan=2)

        self.patientGenderLabel.grid(row=3, column=0, columnspan=2)

        self.patientIDLabel.grid(row=4, column=0, columnspan=2)

        self.dropDownMonths.grid(row=5, column=0,  sticky='e')
        self.selectMonthButton.grid(row=5, column=1 , sticky='w')

        self.detailsListbox.grid(row=6, column=0,columnspan=2 )
        self.scrollbarListbox.grid(row=6,column=1, sticky= tk.N + tk.S )
        self.plot()
        self.backButton.grid(row=9, column=0, columnspan=2 )

        
    def back(self):
        self.parent.toPatientsList()

    
    def filterMonth(self):
        return


    def getMedicalData(self):
        observationsResources = self.client.resources('Observation')
        self.observations = observationsResources.search().fetch_all()
        self.observations = [observation for observation in self.observations if observation["subject"].reference == self.patientID]

        medicationResources = self.client.resources('MedicationRequest')
        medications = medicationResources.fetch_all()
        medication = [medication for medication in medications if medication["subject"].reference == self.patientID]

        for observation in self.observations:
            date = observation["issued"]
            date = date.split("T")[0]
            date = date[:-3]
            observationTextList = []

            display  = observation["code"]["coding"][0].display

            valueList = []
            try:
                valueList.append(str(observation["valueQuantity"].value))
            except:
                try:
                    for i in range(len(observation["component"])):
                        valueList.append(str(observation["component"][i]["valueQuantity"].value))
                except:
                    continue

            unitList = []
            try:
                unitList.append(str(observation["valueQuantity"].unit))
            except:
                try:
                    for i in range(len(observation["component"])):
                        unitList.append(str(observation["component"][i]["valueQuantity"].unit))
                except:
                    continue

            for i in range(len(valueList)):
                observationText = "OBSERVATION: " + display + ", VALUE: "  + valueList[i] + " " + unitList[i]
                observationTextList.append(observationText)

            for i in range(len(observationTextList)):   
                if date in self.observationToDateDict:
                    self.observationToDateDict[date].append(observationTextList[i])
                elif date not in self.observationToDateDict:
                    self.observationToDateDict[date] = [observationTextList[i]]

        for medication in medications:
            date = medication["authoredOn"]
            date = date.split("T")[0]
            date = date[:-3]
            observationTextList = []

            display =  medication["medicationCodeableConcept"]["coding"][0].display
            medicationText = "MEDICATION: " + display
            if date in self.observationToDateDict:
                self.observationToDateDict[date].append(medicationText)
            elif date not in self.observationToDateDict:
                self.observationToDateDict[date] = [medicationText]
            


    def fillListBox(self, medicalData):
        for data in medicalData:
            self.detailsListbox.insert(0, data)


    def clearAndFillNewMonth(self):
        month = self.clicked.get()
        self.detailsListbox.delete(0, tk.END)
        self.fillListBox(self.observationToDateDict[month])

    def plot(self):
        fig = Figure(figsize=(6,6), dpi=100)
        observationsResources = self.client.resources('Observation')
        observationsResources = observationsResources.search(subject = self.patientID).sort('date')
        observations = observationsResources.fetch_all()
        observations = [observation for observation in self.observations if observation["code"].text == "Body Weight"]
        dates = []
        weightValues = []
        for observation in observations:
            dates.append(observation["issued"].split("T")[0])
            weightValues.append(float(str(observation["valueQuantity"].value)[:4]))
        y = weightValues
  
        plot1 = fig.add_subplot(111)

        plot1.plot(dates, y)

        plot1.set_title("Body weight kg")
        plot1.tick_params(axis = "x", which= "major", labelsize=6, labelrotation=90)

        canvas = FigureCanvasTkAgg(fig,
                                master = self)  
        canvas.draw()
    
        canvas.get_tk_widget().grid(row=7,column=0, columnspan=2)
    
        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=8,column=0, columnspan=2)
        toolbar = NavigationToolbar2Tk(canvas,
                                    toolbarFrame)
        toolbar.update()  
    
        
  