from pages.shared import *

class SettingsPage(ttk.Frame):
    def __init__(self, parent, model_file=resource_path("data/model.pkl")):
        super().__init__(parent)
        self.model_file = model_file
        self.current_language = current_language
        self.create_widgets()
    
    def create_widgets(self):
        self.title = ttk.Label(self, text=get_translation("settings_title"), font=("Arial", 14))
        self.title.pack(pady=10)

        # Language selection frame
        lang_frame = ttk.Frame(self)
        lang_frame.pack(pady=5, padx=10, fill="x")
        lang_label = ttk.Label(lang_frame, text=get_translation("choose_language"))
        lang_label.pack(side="left")
        self.lang_dropdown = ttk.Combobox(lang_frame, 
                                          values=list(translations.keys()), 
                                          state="readonly")
        self.lang_dropdown.set(self.current_language)
        self.lang_dropdown.bind("<<ComboboxSelected>>", self.on_language_change)
        self.lang_dropdown.pack(side="left", padx=5)
        self.selected_lang_label = ttk.Label(lang_frame, text="")
        self.selected_lang_label.pack(side="left", padx=5)
        
        # Import Model Section
        self.import_frame = ttk.LabelFrame(self, text=get_translation("import_model"))
        self.import_frame.pack(fill="x", padx=10, pady=5)
        self.import_button = ttk.Button(self.import_frame, text=get_translation("import_model"), 
        command=self.import_model)
        self.import_button.pack(padx=10, pady=10)
        
        # Export Model Section
        self.export_frame = ttk.LabelFrame(self, text=get_translation("export_model"))
        self.export_frame.pack(fill="x", padx=10, pady=5)
        self.export_button = ttk.Button(self.export_frame, text=get_translation("export_model"), command=self.export_model)
        self.export_button.pack(padx=10, pady=10)
        
        # Status Label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_var, wraplength=400)
        status_label.pack(pady=10)

    def on_language_change(self, event):
        selected_lang = self.lang_dropdown.get()
        self.current_language = selected_lang
        set_current_language(selected_lang)
        self.selected_lang_label.config(text=get_translation("selected_language"))


    
    def import_model(self):
        # Open a file dialog to select a .pkl file to import.
        file_path = filedialog.askopenfilename(title=get_translation("settings_1"), filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            try:
                os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
                shutil.copy2(file_path, self.model_file)
                self.status_var.set(get_translation("settings_2"))

            except Exception as e:
                self.status_var.set(f"{get_translation("settings_3")} {e}")
        else:
            self.status_var.set(get_translation("settings_4"))
    
    def export_model(self):
        # Open a folder dialog to select a destination folder for exporting the model.
        folder = filedialog.askdirectory(title=get_translation("settings_5"))
        if folder:
            try:
                destination = os.path.join(folder, os.path.basename(self.model_file))
                shutil.copy2(self.model_file, destination)
                self.status_var.set(f"{get_translation("settings_6")} {destination}.")
            except Exception as e:
                self.status_var.set(f"{get_translation("settings_7")} {e}")
        else:
            self.status_var.set(get_translation("settings_8"))

if __name__ == "__main__":
    root = tk.Tk()
    root.title(get_translation("settings_title"))
    root.geometry("400x300")
    settings_page = SettingsPage(root)
    settings_page.pack(expand=True, fill="both")
    root.mainloop()
