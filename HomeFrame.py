import tkinter as tk
from fhirpy import SyncFHIRClient

class HomeFrame(tk.Frame):
    def __init__(self, parent, client):
        tk.Frame.__init__(self, parent)
        self.client = client
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.title = tk.Label(self, text="SELECT PATIENT", font=('Helvetica bold', 40))
        self.scrollbar = tk.Scrollbar(self, orient='vertical')
        self.my_listbox = tk.Listbox(self, width= 50, height= 5, yscrollcommand= self.scrollbar.set)
        self.lastnameInput = tk.Entry(self, width=20)
        self.findByNameTextField = tk.Label(self, text="FIND BY LASTNAME:", font = ('Helvetica', 10))
        self.filterButton = tk.Button(self, text='filter', command= self.filter)
        self.infoButton = tk.Button(self, text="INFO", command = self.info)

        self.scrollbar.config(command=self.my_listbox.yview)


        self.title.grid(row=0, column= 0, columnspan=2)
        
        self.findByNameTextField.grid(row=1, column=0, sticky='e')
        self.lastnameInput.grid(row=1, column=1, sticky='w')
        
        self.filterButton.grid(row= 2, column=0, columnspan=2 )
        
        self.my_listbox.grid(row=3, column = 0, columnspan=2 )
        self.scrollbar.grid(row= 3,column=1, sticky= tk.N + tk.S)
        
        self.infoButton.grid(row=4, column=0, columnspan=2)


        
        self.patients = self.getPatientsNames(client)
        getFamilyName = lambda patient: patient['name'][0].family
        self.patientNames = [ getFamilyName(patient) for patient in self.patients ]
        self.fillListBox(self.patientNames)
        

    def getPatientsNames(self, client):
        resources = client.resources('Patient')
        patients = resources.search().fetch_all()
        # patients = resources.fetch()
        return patients
        

    def info(self):
            selectedPatientName = str(self.my_listbox.get(tk.ANCHOR))
            if selectedPatientName == '':
                return
            resources = self.client.resources('Patient')
            resources =  resources.search(name= selectedPatientName)
            patient = resources.fetch()
            self.parent.changeToPatientInfo(patient)


    def filter(self):
        filterStr = self.lastnameInput.get()
        filterNames = [name for name in self.patientNames if name.startswith(filterStr)]
        self.my_listbox.delete(0, tk.END)
        self.fillListBox(filterNames)


    def fillListBox(self, names):
        for name in names:
            self.my_listbox.insert(0, name)
