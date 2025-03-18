from pages.shared import *

class WorkPage(ttk.Frame):
    def __init__(self, parent,
                 model_file=resource_path("data/model.pkl"),
                 output_txt=resource_path("data/generated_spss.txt"),
                 output_csv=resource_path("data/generated_data.csv"),
                 output_json=resource_path("data/generated_data.json")):
        super().__init__(parent)
        self.model_file = model_file
        self.output_txt = output_txt
        self.output_csv = output_csv
        self.output_json = output_json
        # Predefined type options (should match those used in training)
        self.type_options = option_dropdown
        self.selected_folder = ""
        self.create_widgets()
        self.model_loaded = False
        self.load_model()

    def create_widgets(self):
        title = ttk.Label(self, text=get_translation("generate_spss_title"), font=("Arial", 14))
        title.pack(pady=10)

        # Folder selection frame
        folder_frame = ttk.Frame(self)
        folder_frame.pack(pady=5, fill='x', padx=10)
        browse_button = ttk.Button(folder_frame, text=get_translation("generate_spss_1"), command=self.browse_folder)
        browse_button.pack(side='left')
        self.folder_label = ttk.Label(folder_frame, text=get_translation("generate_spss_2"), wraplength=300)
        self.folder_label.pack(side='left', padx=10)

        generate_button = ttk.Button(self, text=get_translation("generate_spss_3"), command=self.generate_spss)
        generate_button.pack(pady=10)

        self.status_var = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_var, wraplength=400)
        status_label.pack(pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.folder_label.config(text=os.path.basename(folder))
            self.status_var.set(get_translation("generate_spss_4"))
        else:
            self.status_var.set(get_translation("generate_spss_5"))

    def load_model(self):
        if not os.path.exists(self.model_file):
            self.status_var.set(get_translation("generate_spss_6"))
            return
        try:
            with open(self.model_file, 'rb') as f:
                model_data = pickle.load(f)
                # Handle both dictionary and tuple formats.
                if isinstance(model_data, dict):
                    self.vectorizer = model_data.get("vectorizer")
                    self.clf = model_data.get("clf")
                else:
                    # Assume tuple: (vectorizer, clf)
                    self.vectorizer, self.clf = model_data
            self.model_loaded = True
            self.status_var.set(get_translation("generate_spss_7"))
        except Exception as e:
            self.status_var.set(f"{get_translation("generate_spss_8")} {e}")
            self.model_loaded = False

    def predict_spss(self, ascx_content):
        """
        Determine the predicted type (by checking if any known type is mentioned in the content).
        If none is found, default to the first type option.
        Then, combine the ascx content with the predicted type and predict the SPSS output.
        """
        predicted_type = None
        for option in self.type_options:
            if option.lower() in ascx_content.lower():
                predicted_type = option
                break
        if not predicted_type:
            predicted_type = self.type_options[0]
        input_text = ascx_content + " " + predicted_type
        try:
            X_vect = self.vectorizer.transform([input_text])
            pred = self.clf.predict(X_vect)[0]
        except Exception as e:
            pred = f"{get_translation("generate_spss_9")} {e}"
        return predicted_type, pred

    def generate_spss(self):
        if not self.selected_folder:
            self.status_var.set(get_translation("generate_spss_10"))
            return
        if not self.model_loaded:
            self.status_var.set(get_translation("generate_spss_11"))
            return
        
        # Prompt for an output folder for the spss.txt file.
        txt_output_folder = filedialog.askdirectory(title=get_translation("generate_spss_12"))
        if not txt_output_folder:
            self.status_var.set(get_translation("generate_spss_13"))
            return

        out_txt = os.path.join(txt_output_folder, "generated_spss.txt")
        # The CSV and JSON files remain stored in the default data folder.
        out_csv = self.output_csv  # e.g., "./data/generated_data.csv"
        out_json = self.output_json  # e.g., "./data/generated_data.json"

        generated_records = {}  # For JSON
        output_lines = []       # For spss.txt
        generated_csv_rows = [] # For CSV

        # Iterate through all ASCX files in the selected folder
        for root, dirs, files in os.walk(self.selected_folder):
            for filename in files:
                if filename.lower().endswith('.ascx'):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except Exception as e:
                        self.status_var.set(f"{get_translation("generate_spss_14")} {filename}: {e}")
                        continue

                    predicted_type, predicted_spss = self.predict_spss(content)
                    # For spss.txt, we output the filename and predicted SPSS output.
                    output_lines.append(f"{filename}: {predicted_spss}")
                    # For CSV, store the ascx content, predicted type, and predicted spss.
                    generated_csv_rows.append([content, predicted_type, predicted_spss])
                    # For JSON, use incremental numeric keys.
                    record_id = str(len(generated_records) + 1)
                    generated_records[record_id] = {
                        "ascx": content,
                        "type": predicted_type,
                        "spss": predicted_spss
                    }

        # Write spss.txt
        try:
            os.makedirs(os.path.dirname(self.output_txt), exist_ok=True)
            with open(out_txt, 'w', encoding='utf-8') as f:
                f.write("\n".join(output_lines))
        except Exception as e:
            self.status_var.set(f"{get_translation("generate_spss_15")} {e}")
            return

        # Write CSV file
        try:
            os.makedirs(os.path.dirname(out_csv), exist_ok=True)
            with open(out_csv, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ascx", "type", "spss"])
                writer.writerows(generated_csv_rows)
        except Exception as e:
            self.status_var.set(f"{get_translation("generate_spss_16")} {e}")
            return

        # Write JSON file
        try:
            os.makedirs(os.path.dirname(out_json), exist_ok=True)
            with open(out_json, 'w', encoding='utf-8') as f:
                json.dump(generated_records, f, indent=4)
        except Exception as e:
            self.status_var.set(f"{get_translation("generate_spss_17")} {e}")
            return

        self.status_var.set(
            f"{get_translation("generate_spss_18")}"
            f"{os.path.basename(self.output_txt)}, {os.path.basename(self.output_csv)}, and {os.path.basename(self.output_json)}."
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.title(get_translation("generate_spss_title"))
    root.geometry("600x400")
    work_page = WorkPage(root)
    work_page.pack(expand=True, fill='both')
    root.mainloop()
