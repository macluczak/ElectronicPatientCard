import tkinter as tk


from rsa import verify
import HomeFrame as hf
import Info as info

from fhirpy import SyncFHIRClient
from fhirpy import AsyncFHIRClient
import aiohttp
import ssl


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        _ = {
            "ssl": ssl.create_default_context(),
            "timeout": aiohttp.ClientTimeout(total=100),
        }
        _ = {
            "verify": False,
            "allow_redirects": True,
            "timeout": 60,
        }
        icon = tk.PhotoImage(file='cardiogram1.png')

        HAPI_BASE_URL = "http://localhost:8080/baseR4"

        self.grid_columnconfigure(0, weight=1)
        self.client = SyncFHIRClient(HAPI_BASE_URL)
        self.title("Electronic Patient Card")
        self.geometry("1200x675")
        self.iconphoto(True, icon)

        self.infoFrame = type('info.Info', (), {})
        self.homeFrame = hf.HomeFrame(self, self.client)


        # self.homeFrame.pack(fill='both', expand=1)
        self.homeFrame.place(x=0, y=0, height= 675, width=1200)



        # observationsResources = self.client.resources('Observation')
        # observationsResources = observationsResources.search()
        # self.observations = observationsResources.fetch()
        # for observation in self.observations:
        #     print(observation)

    def changeToPatientInfo(self, patient):
        self.infoFrame = info.Info(self, self.client, patient)
        self.infoFrame.pack(fill='both', expand=1)
        self.homeFrame.forget()

    def toPatientsList(self):
        self.homeFrame.pack(fill='both', expand=1)
        self.infoFrame.forget()


def main():
    app = App()
    app.resizable(0, 0)
    app.mainloop()



if __name__ == "__main__":
    main()
