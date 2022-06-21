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
        aiohttp_config = {
            "ssl": ssl.create_default_context(),
            "timeout": aiohttp.ClientTimeout(total=100),
        }
        requests_config = {
            "verify": False,
            "allow_redirects": True,
            "timeout": 60,
        }
        self.icon = tk.PhotoImage(file='icon2.png')

        HAPI_BASE_URL = "http://localhost:8080/baseR4"
        self.client = SyncFHIRClient(HAPI_BASE_URL)

        self.grid_columnconfigure(0, weight=1)
        self.title("Electronic Patient Card")
        self.geometry("1400x1000")
        self.iconphoto(True, self.icon)

        # self.myCanvas = tk.Canvas(self)
        # self.myCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # self.frameScrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.myCanvas.yview)
        # self.frameScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # self.myCanvas.configure(yscrollcommand=self.frameScrollbar.set)
        # self.myCanvas.bind('<Configure>', lambda e: self.myCanvas.configure(scrollregion=self.myCanvas.bbox("all")))

        self.infoFrame = type('info.Info', (), {})
        self.homeFrame = hf.HomeFrame(self, self.client)
        # self.myCanvas.create_window((0,0), window=self.homeFrame, anchor="nw")
        self.homeFrame.pack(fill='both', expand=1)
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
    app.mainloop()


if __name__ == "__main__":
    main()
