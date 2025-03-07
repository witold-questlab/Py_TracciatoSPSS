from pages.shared import *

class UpdatePage(ttk.Frame):
    def __init__(self, parent,
                 generated_json_file="./data/generated_data.json",
                 training_csv="./data/training_data.csv",
                 training_json="./data/training_data.json",
                 model_file="./data/model.pkl"):
        super().__init__(parent)
        self.generated_json_file = generated_json_file
        self.training_csv = training_csv
        self.training_json = training_json
        self.model_file = model_file
        
        ensure_csv_exists(self.training_csv)
        ensure_json_exists(self.training_json)
        
        # Load candidate records from generated_data.json
        self.generated_data = self.load_generated_data()
        self.record_keys = list(self.generated_data.keys())
        self.current_index = 0
        
        # Predefined type options (should match those used in training)
        self.type_options = ["altro", "radio", "sino & co", "checklist", "matrice", "textlist", "matrice verticale", "matrice primosecondo", "rating", "matrice rating"]
        
        self.create_widgets()
        self.load_current_record()
        
    def load_generated_data(self):
        try:
            with open(self.generated_json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Error loading generated data: {e}")
            return {}
        
    def create_widgets(self):
        title = ttk.Label(self, text="Update Training Model", font=("Arial", 14))
        title.pack(pady=10)
        
        # Navigation frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=5)
        prev_button = ttk.Button(nav_frame, text="Previous", command=self.show_previous)
        prev_button.pack(side="left", padx=5)
        next_button = ttk.Button(nav_frame, text="Next", command=self.show_next)
        next_button.pack(side="left", padx=5)
        
        # Label to indicate record number
        self.record_label = ttk.Label(nav_frame, text="Record 0/0")
        self.record_label.pack(side="left", padx=10)
        
        # ASCX content
        ascx_label = ttk.Label(self, text="ASCX Content:")
        ascx_label.pack(anchor='w', padx=10)
        self.ascx_text = tk.Text(self, height=10)
        self.ascx_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Type dropdown
        type_frame = ttk.Frame(self)
        type_frame.pack(pady=5, padx=10, fill='x')
        type_label = ttk.Label(type_frame, text="Type:")
        type_label.pack(side="left")
        self.type_dropdown = ttk.Combobox(type_frame, values=self.type_options, state="readonly")
        self.type_dropdown.pack(side="left", padx=5)
        
        # SPSS Equivalent
        spss_label = ttk.Label(self, text="SPSS Equivalent:")
        spss_label.pack(anchor='w', padx=10)
        self.spss_text = tk.Text(self, height=5)
        self.spss_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Button to update the candidate record in training data (CSV and JSON)
        update_record_button = ttk.Button(self, text="Update Record", command=self.update_record)
        update_record_button.pack(pady=5)
        
        # Separate button to update (retrain) the model with all training data
        update_model_button = ttk.Button(self, text="Update Model", command=self.update_model)
        update_model_button.pack(pady=5)
        
        self.status_var = tk.StringVar()
        status_label = ttk.Label(self, textvariable=self.status_var, wraplength=400)
        status_label.pack(pady=5)
        
    def load_current_record(self):
        if not self.record_keys:
            self.status_var.set("No generated records to update.")
            self.clear_fields()
            self.record_label.config(text="Record 0/0")
            return
        
        key = self.record_keys[self.current_index]
        record = self.generated_data.get(key, {})
        self.ascx_text.delete("1.0", tk.END)
        self.ascx_text.insert(tk.END, record.get("ascx", ""))
        self.type_dropdown.set(record.get("type", self.type_options[0]))
        self.spss_text.delete("1.0", tk.END)
        self.spss_text.insert(tk.END, record.get("spss", ""))
        self.record_label.config(text=f"Record {self.current_index+1}/{len(self.record_keys)}")
        self.status_var.set("")
        
    def clear_fields(self):
        self.ascx_text.delete("1.0", tk.END)
        self.type_dropdown.set(self.type_options[0])
        self.spss_text.delete("1.0", tk.END)
        
    def show_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_record()
        else:
            self.status_var.set("Already at the first record.")
        
    def show_next(self):
        if self.current_index < len(self.record_keys) - 1:
            self.current_index += 1
            self.load_current_record()
        else:
            self.status_var.set("Already at the last record.")
            
    def update_record(self):
        """
        Take the current inputs, append them to training data (CSV and JSON),
        and update the model by retraining on the full training data.
        """
        ascx_val = self.ascx_text.get("1.0", tk.END).strip()
        type_val = self.type_dropdown.get().strip()
        spss_val = self.spss_text.get("1.0", tk.END).strip()
        if not ascx_val or not type_val or not spss_val:
            self.status_var.set("All fields must be filled before updating.")
            return
        
        # Append record to training CSV
        try:
            with open(self.training_csv, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([ascx_val, type_val, spss_val])
        except Exception as e:
            self.status_var.set(f"Error updating training CSV: {e}")
            return
        
        # Append record to training JSON
        try:
            with open(self.training_json, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
        except Exception as e:
            self.status_var.set(f"Error reading training JSON: {e}")
            return
        
        try:
            existing_ids = [int(k) for k in training_data.keys()] if training_data else [0]
            new_id = str(max(existing_ids) + 1)
        except Exception:
            new_id = "1"
        
        training_data[new_id] = {
            "ascx": ascx_val,
            "type": type_val,
            "spss": spss_val
        }
        
        try:
            with open(self.training_json, 'w', encoding='utf-8') as f:
                json.dump(training_data, f, indent=4)
        except Exception as e:
            self.status_var.set(f"Error updating training JSON: {e}")
            return
        
        self.status_var.set(f"Record updated and added as ID {new_id} in training data.")
        
    def update_model(self):
        """Retrain the model using all training data from the training JSON file."""
        try:
            with open(self.training_json, 'r', encoding='utf-8') as f:
                training_data = json.load(f)
        except Exception as e:
            self.status_var.set(f"Error reading training JSON for model update: {e}")
            return
        
        X_train = []
        y_train = []
        for record in training_data.values():
            input_text = record.get("ascx", "") + " " + record.get("type", "")
            X_train.append(input_text)
            y_train.append(record.get("spss", ""))
        
        if not X_train or not y_train:
            self.status_var.set("Training data incomplete, model not updated.")
            return
        
        vectorizer = CountVectorizer()
        X_train_vect = vectorizer.fit_transform(X_train)
        clf = MultinomialNB()
        clf.fit(X_train_vect, y_train)
        
        model_data = {
            "vectorizer": vectorizer,
            "clf": clf,
            "trained_ids": list(training_data.keys())
        }
        os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
        try:
            with open(self.model_file, "wb") as f:
                pickle.dump(model_data, f)
            self.status_var.set("Model updated successfully.")
        except Exception as e:
            self.status_var.set(f"Error saving updated model: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Update Training Model")
    root.geometry("800x600")
    update_page = UpdatePage(root)
    update_page.pack(expand=True, fill='both')
    root.mainloop()
