import tkinter.font as font
import tkinter as tk
from PIL import Image, ImageTk
from fhirpy import SyncFHIRClient


class HomeFrame(tk.Frame):
    def __init__(self, parent, client):
        tk.Frame.__init__(self, parent)

        my_font = font.Font(family="Lato")
        color_background = "#EDF2F4"  # light gray
        color_primary = "#D90429"  # dark red
        color_secondary = "#EF233C"  # red
        color_text = "#2B2D42"  # light black
        color_special = "#8D99AE"  # gray

        self.config(background=color_background)
        self.client = client
        self.parent = parent
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.imageHeart = Image.open('cardiogram2.png')
        self.image_resize = self.imageHeart.resize((70, 70), Image.ANTIALIAS)
        self.logo = ImageTk.PhotoImage(self.image_resize)

        self.imageScope = Image.open('magnifier.png')
        self.image_resize = self.imageScope.resize((28, 28), Image.ANTIALIAS)
        self.scope = ImageTk.PhotoImage(self.image_resize)

        self.imageUser = Image.open('user0.png')
        self.image_resize = self.imageUser.resize((28, 28), Image.ANTIALIAS)
        self.userIcon = ImageTk.PhotoImage(self.image_resize)

        self.imageScope = Image.open('love.png')
        self.image_resize = self.imageScope.resize((650, 650), Image.ANTIALIAS)
        self.love = ImageTk.PhotoImage(self.image_resize)

        self.nav_background = tk.Label(self,
                                       background=color_secondary
                                       )

        self.nav_label = tk.Label(self,
                                  text="Electronic Patient Card",
                                  font=(my_font, 20, 'bold'),
                                  width="600",
                                  background=color_secondary,
                                  image=self.logo,
                                  compound='left',

                                  padx=20,
                                  pady=20,
                                  fg="white",
                                  anchor="w")

        self.searchButton = tk.Button(self,
                                      text="Search",
                                      font=(my_font, 10, 'bold'),
                                      compound='top',
                                      fg='white',
                                      activeforeground=color_background,
                                      image=self.scope,
                                      command=self.filter,
                                      background=color_secondary,
                                      activebackground=color_primary,
                                      padx=3,
                                      pady=3
                                      )
        self.nameInput = tk.Entry(self,

                                  font=(my_font, 18, 'bold'),
                                  fg=color_text

                                  )

        self.background_label = tk.Label(self,
                                         background=color_background,
                                         image=self.love
                                         )

        # self.title = tk.Label(self, text="SELECT PATIENT", font=('Helvetica bold', 40), background=color_background)

        self.scrollbar = tk.Scrollbar(self,

                                      orient='vertical',
                                      background=color_special,
                                      )

        self.listTitle = tk.Label(self,

                                  text="Select a patient to view details",
                                  background=color_background,
                                  font=(my_font, 18, 'bold'),
                                  fg=color_text
                                  )

        self.my_listbox = tk.Listbox(self,
                                     width=50,

                                     font=(my_font, 12, 'bold'),
                                     fg=color_text,
                                     background='white',

                                     selectbackground=color_special,
                                     selectforeground='white',

                                     yscrollcommand=self.scrollbar.set)

        self.detailButton = tk.Button(self,
                                      text="Details",
                                      command=self.detail,
                                      background='white',
                                      activebackground=color_special,
                                      font=(my_font, 10, 'bold'),
                                      compound='top',
                                      fg=color_text,
                                      activeforeground=color_background,
                                      image=self.userIcon,
                                      padx=3,
                                      pady=3
                                      )

        self.background_label.place(x=-250, y=120, width=650, height=650)
        self.nav_background.place(x=0, y=0, width=1200, height=120)

        self.nav_label.grid(row=0, column=0, sticky="w", columnspan=1)

        # self.title.grid(row=1, column=0, columnspan=2)
        self.scrollbar.config(command=self.my_listbox.yview)

        self.searchButton.grid(row=0, column=1, sticky='e', padx=10)
        self.nameInput.grid(row=0, column=2, sticky='w')

        self.listTitle.grid(row=2, column=1, columnspan=2, sticky='s', pady=(50,0), padx=(40,0))
        self.my_listbox.grid(row=3, column=1, columnspan=2, sticky='e', pady=(0,20))
        self.scrollbar.grid(row=3, column=3, sticky="w")

        self.detailButton.grid(row=4, column=2, columnspan=1, sticky='e')


        self.patients = self.getPatientsNames(client)
        getFamilyName = lambda patient: patient['name'][0].family
        self.patientNames = [getFamilyName(patient) for patient in self.patients]
        self.fillListBox(self.patientNames)

    def getPatientsNames(self, client):
        resources = client.resources('Patient')
        patients = resources.search().fetch_all()
        return patients

    def detail(self):
        selectedPatientName = str(self.my_listbox.get(tk.ANCHOR))
        if selectedPatientName == '':
            return
        resources = self.client.resources('Patient')
        resources = resources.search(name=selectedPatientName)
        patient = resources.fetch()
        self.parent.changeToPatientInfo(patient)

    def filter(self):
        filterStr = self.nameInput.get()
        filterNames = [name for name in self.patientNames if name.startswith(filterStr)]
        self.my_listbox.delete(0, tk.END)
        self.fillListBox(filterNames)

    def fillListBox(self, names):
        for name in names:
            self.my_listbox.insert(0, name)
