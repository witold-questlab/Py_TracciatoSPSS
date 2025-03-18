from pages.shared import *

class TrainPage(ttk.Frame):
    def __init__(self, parent, 
                 csv_file=resource_path("data/training_data.csv"),
                 json_file=resource_path("data/training_data.json"),                   
                 model_file=resource_path("data/model.pkl")):
        super().__init__(parent)
        self.csv_file = csv_file
        self.json_file = json_file
        self.model_file = model_file
        ensure_csv_exists(self.csv_file)
        ensure_json_exists(self.json_file)
        self.ascx_content = ""
        self.type_options = option_dropdown
        self.create_widgets()

    def create_widgets(self):
        title = ttk.Label(self, text=get_translation("train_1"), font=("Arial", 14))
        title.pack(pady=10)

        # Frame for file selection
        file_frame = ttk.Frame(self)
        file_frame.pack(pady=5, fill='x', padx=10)
        browse_button = ttk.Button(file_frame, text=get_translation("train_2"), command=self.browse_file)
        browse_button.pack(side='left')
        self.file_label = ttk.Label(file_frame, text=get_translation("train_3"), wraplength=300)
        self.file_label.pack(side='left', padx=10)

        # Entry for "Type" (single-line input)
        type_frame = ttk.Frame(self)
        type_frame.pack(pady=5, fill='x', padx=10)
        type_label = ttk.Label(type_frame, text=get_translation("update_type"))
        type_label.pack(side='left')
        self.type_dropdown = ttk.Combobox(type_frame, values=self.type_options, state="readonly")
        self.type_dropdown.set(self.type_options[0])
        self.type_dropdown.pack(side='left', padx=5)

# Frame for SPSS VARIABLE LABEL input
        var_label_frame = ttk.Frame(self)
        var_label_frame.pack(pady=5, fill='x', padx=10)
        var_label_label = ttk.Label(var_label_frame, text="VARIABLE LABEL:")
        var_label_label.pack(anchor='w')
        self.var_label_text = tk.Text(var_label_frame, height=3)
        self.var_label_text.pack(fill='x', padx=5)

        # Frame for SPSS VALUE LABEL input
        val_label_frame = ttk.Frame(self)
        val_label_frame.pack(pady=5, fill='x', padx=10)
        val_label_label = ttk.Label(val_label_frame, text="VALUE LABEL:")
        val_label_label.pack(anchor='w')
        self.val_label_text = tk.Text(val_label_frame, height=3)
        self.val_label_text.pack(fill='x', padx=5)

        # Button to add the record to CSV and JSON
        add_button = ttk.Button(self, text=get_translation("train_4"), command=self.add_record)
        add_button.pack(pady=10)

        # Separator
        separator = ttk.Separator(self, orient='horizontal')
        separator.pack(fill='x', padx=10, pady=10)

        # Button to train the model
        train_button = ttk.Button(self, text=get_translation("train_5"), command=self.train_model)
        train_button.pack(pady=10)

        # Status message label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_var)
        status_label.pack(pady=10)
    
    def browse_file(self):
        """Open a file dialog limited to ASCX files and load its content."""
        file_path = filedialog.askopenfilename(filetypes=[("ASCX Files", "*.ascx")])
        if file_path:
            self.file_label.config(text=os.path.basename(file_path))
            try:
                with open(file_path, 'r', encoding='utf-8', errors="replace") as f:
                    raw_content = f.read()
                self.ascx_content = extract_fieldset(raw_content)
                self.status_var.set(get_translation("train_6"))
            except Exception as e:
                self.status_var.set(f"{get_translation("train_7")} {e}")
                self.ascx_content = ""
        else:
            self.status_var.set(get_translation("train_8"))
    
    def add_record(self):
        """Add a new record to both the CSV and JSON files."""
        if not self.ascx_content:
            self.status_var.set(get_translation("train_9"))
            return

        # Get user inputs
        type_value = self.type_dropdown.get().strip()
        # Retrieve SPSS variable label text and ensure it starts with "VARIABLE LABEL"
        var_text = self.var_label_text.get("1.0", tk.END).strip()
        if var_text and "VARIABLE LABEL" not in var_text.upper():
            var_text = "VARIABLE LABEL " + var_text

        # Retrieve SPSS value label text and ensure it starts with "VALUE LABEL"
        val_text = self.val_label_text.get("1.0", tk.END).strip()
        if val_text and not val_text.upper().startswith("VALUE LABEL"):
            val_text = "VALUE LABEL " + val_text

        # Combine the two SPSS fields (using a newline as separator)
        combined_spss = var_text + "\n" + val_text
        if not type_value or not combined_spss.strip():
            self.status_var.set(get_translation("train_10"))
            return

        # Append to CSV
        try:
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([self.ascx_content, type_value, combined_spss])
        except Exception as e:
            self.status_var.set(f"{get_translation("train_11")} {e}")
            return

        # Update JSON file
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            self.status_var.set(f"{get_translation("train_12")} {e}")
            return

        # Generate new record ID (incremental numeric string)
        try:
            existing_ids = [int(k) for k in data.keys()] if data else [0]
            new_id = str(max(existing_ids) + 1)
        except Exception:
            new_id = "1"

        data[new_id] = {
            "ascx": self.ascx_content,
            "type": type_value,
            "spss": combined_spss
        }
        try:
            with open(self.json_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            self.status_var.set(f"{get_translation("train_13")} {e}")
            return

        self.status_var.set(f"Record {new_id} {get_translation("train_14")}")

        # Reset fields
        self.file_label.config(text=get_translation("train_3"))
        self.ascx_content = ""
        self.type_dropdown.set(self.type_options[0])
        self.var_label_text.delete("1.0", tk.END)
        self.val_label_text.delete("1.0", tk.END)

    def train_model(self):
        """Load training data from JSON, train or update the model, and save it.
        
        The training input is built by concatenating the 'ascx' content and the 'type' field.
        The target output is the combined SPSS text.
        If a model already exists, update it only if there are new record IDs.
        """
        try:
            with open(self.json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            self.status_var.set(f"{get_translation("train_15")} {self.json_file}: {e}")
            return

        if not data:
            self.status_var.set(get_translation("train_16"))
            return

        # Prepare training lists.
        # We assume each record has keys: "ascx" for input and "spss" for label.
        X_train = []
        y_train = []
        for record in data.values():
            input_text = record.get("ascx", "") + " " + record.get("type", "")
            X_train.append(input_text)
            y_train.append(record.get("spss", ""))

        # Check if a model already exists and if so, load its trained IDs.
        trained_ids = set()
        if os.path.exists(self.model_file):
            try:
                with open(self.model_file, 'rb') as f:
                    saved = pickle.load(f)
                    # Expecting saved data as a dict with keys: vectorizer, clf, trained_ids.
                    vectorizer = saved.get("vectorizer")
                    clf = saved.get("clf")
                    trained_ids = set(saved.get("trained_ids", []))
            except Exception as e:
                self.status_var.set(f"{get_translation("train_17")} {e}")
                return

        # Determine new record IDs from JSON
        current_ids = set(data.keys())
        new_ids = current_ids - trained_ids

        if not new_ids and trained_ids:
            self.status_var.set(get_translation("train_18"))
            return

        vectorizer = CountVectorizer()
        X_train_vect = vectorizer.fit_transform(X_train)
        clf = MultinomialNB()
        clf.fit(X_train_vect, y_train)

        # Update the trained_ids to include all current IDs
        trained_ids = list(current_ids)

        # Save the updated model along with the list of trained IDs.
        model_data = {
            "vectorizer": vectorizer,
            "clf": clf,
            "trained_ids": trained_ids
        }
        os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
        with open(self.model_file, "wb") as f:
            pickle.dump(model_data, f)

        self.status_var.set(f"{get_translation("train_19")} {os.path.basename(self.model_file)}")
