from pages.shared import *
from pages.training_page import TrainPage
from pages.generate_spss import WorkPage
from pages.update_model import UpdatePage
from pages.settings import SettingsPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Creazione Tracciato SPSS")
        self.geometry("1000x600")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')

        # Create the tabs from the separate modules.
        train_page = TrainPage(notebook)
        work_page = WorkPage(notebook)
        update_page = UpdatePage(notebook)
        setting_page = SettingsPage(notebook)

        notebook.add(train_page, text="Train")
        notebook.add(work_page, text="Generate")
        notebook.add(update_page, text="Update")
        notebook.add(setting_page, text="Settings")
        # Set the default tab to Train.
        notebook.select(train_page)

def launch_gui():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    launch_gui()