import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure


class Info(tk.Frame):
    def __init__(self, parent, client, patient):
        tk.Frame.__init__(self, parent)
        self.client = client
        self.parent = parent
        self.patient = patient.pop()
        self.patientID = 'Patient/' + str(self.patient["id"])
        self.observationToDateDict = {}
        self.observations = []
        self.getMedicalData()

        font_LargeBolt = font.Font(family="Lato", size=20, weight="bold")
        font_MediumBolt = font.Font(family="Lato", size=16, weight="bold")
        font_SmallBolt = font.Font(family="Lato", size=12, weight="bold")
        font_XSmallBolt = font.Font(family="Lato", size=10, weight="bold")
        font_XXSmallBolt = font.Font(family="Lato", size=8, weight="bold")

        font_Large = font.Font(family="Lato", size=20, weight="normal")
        font_Medium = font.Font(family="Lato", size=16, weight="normal")
        font_Small = font.Font(family="Lato", size=12, weight="normal")
        font_XSmall = font.Font(family="Lato", size=10, weight="normal")
        font_XXSmall = font.Font(family="Lato", size=8, weight="normal")

        color_background = "#EDF2F4"  # light gray
        color_primary = "#D90429"  # dark red
        color_secondary = "#EF233C"  # red
        color_text = "#2B2D42"  # light black
        color_special = "#8D99AE"  # gray

        self.imageScope = Image.open('love.png')
        self.image_resize = self.imageScope.resize((650, 650), Image.ANTIALIAS)
        self.love = ImageTk.PhotoImage(self.image_resize)

        self.imageUser = Image.open('user1.png')
        self.image_resize = self.imageUser.resize((70, 70), Image.ANTIALIAS)
        self.userIcon = ImageTk.PhotoImage(self.image_resize)

        self.imageScope = Image.open('back.png')
        self.image_resize = self.imageScope.resize((28, 28), Image.ANTIALIAS)
        self.scope = ImageTk.PhotoImage(self.image_resize)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.config(background=color_background)

        self.clicked = tk.StringVar(self)
        self.months = list(self.observationToDateDict.keys())
        self.clicked.set(self.months[0])

        self.background_label = tk.Label(self,
                                         background=color_background,
                                         image=self.love
                                         )
        self.nav_background = tk.Label(self,
                                       background=color_secondary
                                       )

        self.nav_background.place(x=0, y=0, width=1200, height=120)

        self.nav_label = tk.Label(self,
                                  text="Electronic Patient Card",
                                  font=font_LargeBolt,
                                  background=color_secondary,
                                  image=self.userIcon,
                                  compound='left',
                                  padx=20,
                                  pady=20,
                                  fg="white",
                                  anchor="w")

        self.nav_gender = tk.Label(self,
                                   text="Electronic Patient Card",
                                   font=font_Large,
                                   background=color_secondary,

                                   pady=20,
                                   fg="white",
                                   anchor="w")

        self.nav_data = tk.Label(self,
                                 text="Electronic Patient Card",
                                 font=font_Large,
                                 background=color_secondary,
                                 padx=20,
                                 pady=20,
                                 fg="white",
                                 anchor="w")

        self.scrollbarListbox = tk.Scrollbar(self,
                                             orient='vertical')
        self.scrollbarHorListbox = tk.Scrollbar(self,
                                                orient='horizontal')
        self.detailsListbox = tk.Listbox(self,
                                         font=font_XXSmall,
                                         fg=color_text,
                                         background='white',
                                         relief="flat",
                                         selectbackground=color_special,
                                         selectforeground='white',
                                         width=90,
                                         height=20,
                                         yscrollcommand=self.scrollbarListbox.set,
                                         xscrollcommand=self.scrollbarHorListbox.set
                                         )

        self.backButton = tk.Button(self,
                                    relief="groove",
                                    text="Back",
                                    font=font_XSmallBolt,
                                    compound='top',
                                    fg=color_text,
                                    activeforeground=color_background,
                                    image=self.scope,
                                    command=self.back,
                                    background=color_background,
                                    activebackground=color_special,
                                    padx=3,
                                    pady=3)

        self.patientIDLabel = tk.Label(self,
                                       background=color_background,
                                       text="",
                                       font=font_Small)

        self.dropDownMonths = tk.OptionMenu(self,

                                            self.clicked,
                                            *self.months)

        self.selectMonthButton = tk.Button(self,

                                           text="SELECT MONTH",

                                           command=self.clearAndFillNewMonth)

        self.fillListBox(self.observationToDateDict[self.months[0]])

        self.scrollbarListbox.config(command=self.detailsListbox.yview)

        self.patientFullname = str(self.patient["name"][0].given[0]) + " " + str(self.patient["name"][0].family)
        self.patiendBirthDateText = " BIRTH DATE: " + str(self.patient["birthDate"])
        self.patientGenderText = "| " + str(self.patient["gender"])
        self.patientIDText = " ID: " + str(self.patient["id"])

        self.nav_label['text'] = self.patientFullname
        self.nav_data['text'] = self.patiendBirthDateText
        self.nav_gender['text'] = self.patientGenderText

        self.patientIDLabel['text'] = self.patientIDText

        self.background_label.place(x=-250, y=120, width=650, height=650)
        self.nav_label.grid(row=0, column=0, sticky="w", columnspan=1)
        self.nav_gender.grid(row=0, column=1, sticky="w", columnspan=1)
        self.nav_data.grid(row=0, column=3, columnspan=1, sticky="e", padx=(50, 0))

        self.detailsListbox.grid(row=1, column=0, columnspan=2, padx=(30, 0), pady=(80, 0))
        self.scrollbarListbox.grid(row=1, column=2, sticky=tk.N + tk.S, pady=(130, 50))
        self.scrollbarHorListbox.grid(row=1, column=0, rowspan=2, columnspan=2, sticky=tk.SE + tk.SW, padx=(55, 30),
                                      pady=(0, 20))

        self.dropDownMonths.place(x=550, y=200)
        self.selectMonthButton.place(x=450, y=203)

        self.backButton.place(x=30, y=600)

        self.plot()
        self.patientIDLabel.place(x=30, y=120)

    def back(self):
        self.parent.toPatientsList()

    def filterMonth(self):
        return

    def getMedicalData(self):
        observationsResources = self.client.resources('Observation')
        self.observations = observationsResources.search().fetch_all()
        self.observations = [observation for observation in self.observations if
                             observation["subject"].reference == self.patientID]

        medicationResources = self.client.resources('MedicationRequest')
        medications = medicationResources.fetch_all()
        medication = [medication for medication in medications if medication["subject"].reference == self.patientID]

        for observation in self.observations:
            date = observation["issued"]
            date = date.split("T")[0]
            date = date[:-3]
            observationTextList = []

            display = observation["code"]["coding"][0].display

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
                observationText = "OBSERVATION: " + display + ", VALUE: " + valueList[i] + " " + unitList[i]
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

            display = medication["medicationCodeableConcept"]["coding"][0].display
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
        fig = Figure(figsize=(6, 6), dpi=80, facecolor="#EDF2F4")
        observationsResources = self.client.resources('Observation')
        observationsResources = observationsResources.search(subject=self.patientID).sort('date')
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
        plot1.tick_params(axis="x", which="major", labelsize=6, labelrotation=90)

        canvas = FigureCanvasTkAgg(fig,
                                   master=self)
        canvas.draw()

        canvas.get_tk_widget().grid(row=1, column=3, columnspan=3, pady=(6, 0), sticky='e')

        toolbarFrame = tk.Frame(master=self, background="#EDF2F4")

        toolbarFrame.place(x=780, y=610)
        toolbar = NavigationToolbar2Tk(canvas,
                                       toolbarFrame)
        toolbar.config(background="#EDF2F4")

        toolbar.update()
