from pages.shared import *

class SettingsPage(ttk.Frame):
    def __init__(self, parent, model_file="./data/model.pkl"):
        super().__init__(parent)
        self.model_file = model_file
        self.create_widgets()
    
    def create_widgets(self):
        title = ttk.Label(self, text="Settings", font=("Arial", 14))
        title.pack(pady=10)
        
        # Import Model Section
        import_frame = ttk.LabelFrame(self, text="Import Model")
        import_frame.pack(fill="x", padx=10, pady=5)
        import_button = ttk.Button(import_frame, text="Import Model", command=self.import_model)
        import_button.pack(padx=10, pady=10)
        
        # Export Model Section
        export_frame = ttk.LabelFrame(self, text="Export Model")
        export_frame.pack(fill="x", padx=10, pady=5)
        export_button = ttk.Button(export_frame, text="Export Model", command=self.export_model)
        export_button.pack(padx=10, pady=10)
        
        # Status Label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_var, wraplength=400)
        status_label.pack(pady=10)
    
    def import_model(self):
        # Open a file dialog to select a .pkl file to import.
        file_path = filedialog.askopenfilename(title="Select Model File", filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            try:
                os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
                shutil.copy2(file_path, self.model_file)
                self.status_var.set("Model imported successfully.")
            except Exception as e:
                self.status_var.set(f"Error importing model: {e}")
        else:
            self.status_var.set("No file selected for import.")
    
    def export_model(self):
        # Open a folder dialog to select a destination folder for exporting the model.
        folder = filedialog.askdirectory(title="Select Export Folder")
        if folder:
            try:
                destination = os.path.join(folder, os.path.basename(self.model_file))
                shutil.copy2(self.model_file, destination)
                self.status_var.set(f"Model exported successfully to {destination}.")
            except Exception as e:
                self.status_var.set(f"Error exporting model: {e}")
        else:
            self.status_var.set("No folder selected for export.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Settings")
    root.geometry("400x300")
    settings_page = SettingsPage(root)
    settings_page.pack(expand=True, fill="both")
    root.mainloop()
